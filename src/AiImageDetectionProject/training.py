import torch
import modelArchitecture as ma
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import time
import datetime
import torchvision.transforms as transforms
import random



def trainingPrep(trainingLoader, validationLoader, epochs, tag):
    model = ma.ModelArch()
    #filePath
    if(tag):
        filePath="/kaggle/working/Machine-Learning-Resume-Project/models/"
    else:
        filePath="models/"
    
    try:
        with (open(filePath+"savedNames.txt", "r")) as file:
            lines = file.readlines()
            if(lines):
                model.load_state_dict(torch.load(filePath+"saves/"  + lines[len(lines)-1].strip(), weights_only=True))
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
    for epoch in range(epochs):
        print("Epoch: " + str(epoch))
        model.train()
        trainingLoss =trainingBlock(trainingLoader, model, optimizer, lossFunction, epoch)
        # print("Trained")
        model.eval()
        accuracy = validationBlock(validationLoader, model, optimizer, lossFunction, epoch)

        print("Epoch: " + str(epoch+1) + "/"+ str(epochs) + " Training Loss: " + str(round(trainingLoss,5)) + " Accuracy: " + str(round(accuracy*100, 3)) + " %") 

        if(accuracy > 0.975 and currentLr == 0.0001):
            print("Accracy Above 90%. Setting Learning Rate To: 0.0001")
            for param_group in optimizer.param_groups:
                param_group['lr'] = 0.00001
                currentLr = 0.00001
        elif(accuracy > 0.95 and currentLr == 0.0005):
            print("Accracy Above 90%. Setting Learning Rate To: 0.0001")
            for param_group in optimizer.param_groups:
                param_group['lr'] = 0.0001
                currentLr = 0.0001
        elif(accuracy > 0.9 and currentLr == 0.001):
            print("Accracy Above 75%. Setting Learning Rate To: 0.0005")
            for param_group in optimizer.param_groups:
                param_group['lr'] = 0.0005
                currentLr = 0.0005

        # if(lastAccuracy < accuracy):
        #     fails = fails+1
        #     print(fails)
        #     if(fails >= 10):
        #         print("Model No Longer Becoming More Accurate")
        #         break
        # else:
        #     fails = 0
        # lastAccuracy = accuracy


        if(accuracy > mostAccurate or epoch%10 == 0):
            if(accuracy > mostAccurate):
                mostAccurate = accuracy
            print(f"Saving the model: ")
            with open(filePath+"savedNames.txt", "a") as file:
                name = "model_" + (time.ctime(time.time()).replace(" ", "_").replace(":", "_"))
                file.write(name + "\n")
                torch.save(model.state_dict(), (filePath+"saves/"+name))        
            

def trainingBlock(trainingLoader, model, optimizer, lossFunction, epochIndex):

    device = torch.device("cuda")

    totalLoss = 0.0

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
        #if (i+1) % 25 == 0:
        #    lastLoss = runningLoss / 25 # loss per batch
        #    print(f'  batch {i + 1} loss: {lastLoss}')
            #tb_x = epochIndex * len(trainingLoader) + i + 1
            #tb_writer.add_scalar('Loss/train', last_loss, tb_x)
        #    runningLoss = 0.0
        #    x=0
            #itemsProcessed -= x

    #print(time.time()-startTime)
    return (totalLoss/len(trainingLoader))

def validationBlock(validationLoader, model, optimizer, lossFunction, epochIndex):
    #print(len(validationLoader))
    device = torch.device("cuda")
    loss = 0.0
    total = 0.0
   
    with torch.no_grad():
        for i, data in enumerate(validationLoader):
            items, labels = data[0].to(device), data[1].float().to(device)

            outputs = model(items)

            probabilities = torch.sigmoid(outputs.view(-1))
            predictions = (probabilities>=0.5).float()

            #print("Predictions")
            #print(predictions.unique(return_counts=True))
            #print("Labels")
            #print(labels.unique(return_counts=True))

            total += (predictions==labels.float().view(-1)).sum().item()
            #print(total)
        print(total)
        print(len(validationLoader.dataset))
        return total/(len(validationLoader.dataset))
            

