import torch
import modelArchitecture as ma
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torch.nn as nn
import time
import datetime
import torchvision.transforms as transforms
import random
import math

minimumLearningRate = 0.000001


def adjustLearningRate(currentLR, currentEpoch, endEpoch):
    return minimumLearningRate + (currentLR-minimumLearningRate)*((1+math.cos((currentEpoch+1)*math.pi/endEpoch))/(1+math.cos((currentEpoch*math.pi)/(endEpoch))))       

# def oldAdjustLearningRate(accuracies, currentLearningRate):

#     increasing = 0
#     massiveJumps = 0
#     decreasing = 0
#     #Loop that tries to detect massive alternating swings in accuracy and lowers the accuracy if they are happening to much
#     for i in range(1, len(accuracies)):
#         if(accuracies[i-1] == 0):
#             #print("Not Enough Data To Adjust Learning Rate")
#             return currentLearningRate
#         if(accuracies[i-1] > accuracies[i]):
#             decreasing+=1
#         else:
#             increasing+=1
#         if(abs(accuracies[i-1]-accuracies[i]) > 0.2):
#             massiveJumps+=1

    
#     print("Alternating: " + str(abs(decreasing-increasing)))
#     print("# Massive Jumps: " + str(massiveJumps))


#     #If the accuracy is either alternating or decreasing alot and there are a significant number of large jumps in accuracy 
#     # then we lower the Learning Rate my a large amount
#     if(abs(decreasing-increasing) <= 1 and massiveJumps > 5):
#         print("Lowering the Learning Rate")
#         currentLearningRate *= 0.20
#     #If there is alot of alternating but not many large jumps then lower the learning rate by a small amounnt
#     elif(abs(decreasing-increasing) <= 1):
#         currentLearningRate *= 0.80
#     #We're getting consistant increases in accuracy raise the learning rate slightly to test if we can aford to traing a bit faster without
#     #overshooting
#     elif(decreasing <= 2):
#         currentLearningRate *= 1.15

#     print(currentLearningRate)
#     return currentLearningRate




def trainingPrep(trainingLoader, validationLoader, epochs, tag):
    model = ma.ModelArch()
    #filePath
    if(tag == 2):
        filePath="/content/Machine-Learning-Resume-Project/models/"
    elif(tag == 1):
        filePath="/kaggle/working/Machine-Learning-Resume-Project/models/"
    else:
        filePath="models/"
    
    try:
        with (open(filePath+"savedNames.txt", "r")) as file:
            lines = file.readlines()
            if(lines):
                print("Found A Model")
                model.load_state_dict(torch.load(filePath+"saves/"  + lines[len(lines)-1].strip(), weights_only=True))
            file.close()
    except IOError:
       print("Didnt Find Any Saved Models") 

    if(torch.cuda.is_available):
        model.to(torch.device("cuda"))
        
    #lossFunction = nn.CrossEntropyLoss()
    lossFunction = nn.BCEWithLogitsLoss()
    
    #Initializes a Adam W optimizer to be used in my training Loop
    currentLr = 0.001
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    #optimizer = torch.optim.SGD(model.parameters())

    # fails = 0
    # lastAccuracy = 1
    mostAccurate = -1
    #previousAccuracies = np.zeros(6)
    for epoch in range(epochs):
        print("Epoch: " + str(epoch+1))
        model.train()
        trainingAccuracy, trainingLoss =trainingBlock(trainingLoader, model, optimizer, lossFunction, epoch)
        # print("Trained")
        model.eval()
        validationAccuracy, validationLoss = validationBlock(validationLoader, model, optimizer, lossFunction, epoch)

        print("Epoch: " + str(epoch+1) + "/"+ str(epochs) + " Training Loss: " + str(round(trainingLoss,5)) + " Training Accuracy: " + str(round(trainingAccuracy*100, 3)) + "% Validation Loss: " + str(round(validationLoss,5)) + " Validation Accuracy: " + str(round(validationAccuracy*100, 3)) + " %") 


        #for i in range(0, 4):
        #    previousAccuracies[i] = previousAccuracies[i+1]
        #previousAccuracies[4] = accuracy
        
        #print("Lowering the ")
        newLr = adjustLearningRate(currentLr, epoch, epochs)
        #print(newLr)
        #Changing the Learning Rate to half the old rate and resetting the previous accuracies rate so we can re check if 
        if(newLr != currentLr):
            for param_group in optimizer.param_groups:
                param_group['lr'] = newLr
                currentLr = newLr

        if(validationAccuracy > mostAccurate or epoch+1%10 == 0 or epoch+1 >= epochs):
            if(validationAccuracy > mostAccurate):
                mostAccurate = validationAccuracy
            print(f"Saving the model: ")
            with open(filePath+"savedNames.txt", "a") as file:
                name = "model_" + str(trainingAccuracy*100)[0:4] + "_" + str(trainingLoss)[0:6] + "_" + str(validationAccuracy*100)[0:4] + "_" + str(validationLoss)[0:6] + "_" + (time.ctime(time.time()).replace(" ", "_").replace(":", "_"))
                file.write(name + "\n")
                torch.save(model.state_dict(), (filePath+"saves/"+name))
                file.close()        
            

def trainingBlock(trainingLoader, model, optimizer, lossFunction, epochIndex):

    device = torch.device("cuda")

    totalLoss = 0.0
    accTotal = 0.0

    # Does this do anything??? I dont remember writing this and I dont know if it does anything but its such a small thing that
    # I'm going to leave it assuming the me who wrote this wasnt totally insane

    # Resseeding the transforms every time we train to avoid the model only learning to distinguish my exact training transforms
    random.seed(time.time())
    #lastLoss=0.0
    #itemsProcessed = len(trainingLoader)
    #x = 0
    #startTime = time.time()
    for i, data in enumerate(trainingLoader):
        items, labels = data[0].to(device), data[1].float().to(device)
        optimizer.zero_grad()


        outputs = model(items)

        loss = lossFunction(outputs, labels)
        loss.backward()

        optimizer.step()
        
        totalLoss += loss.item()
        probabilities = torch.sigmoid(outputs.view(-1))
        predictions = (probabilities>=0.5).float()
        
        accTotal += (predictions==labels.float().view(-1)).sum().item()

    #print(time.time()-startTime)
    return (accTotal/len(trainingLoader.dataset)), (totalLoss/len(trainingLoader))

def validationBlock(validationLoader, model, optimizer, lossFunction, epochIndex):
    #print(len(validationLoader))
    device = torch.device("cuda")
    loss = 0.0
    accTotal = 0.0
    lossTotal = 0.0
   
    with torch.no_grad():
        for i, data in enumerate(validationLoader):
            items, labels = data[0].to(device), data[1].float().to(device)

            outputs = model(items)
            
            probabilities = torch.sigmoid(outputs.view(-1))
            predictions = (probabilities>=0.5).float()

            accTotal += (predictions==labels.float().view(-1)).sum().item()
            lossTotal += lossFunction(outputs, labels).item()
            #print(accTotal)
        print(accTotal)
        print(len(validationLoader))
        return (accTotal/(len(validationLoader.dataset))), (lossTotal/(len(validationLoader)))
            


