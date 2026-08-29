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
        #For running on my local machine
        #with (open("models/savedNames.txt", "r")) as file:
        #For running on the kaggle notebook
        #with (open("/kaggle/working/Machine-Learning-Resume-Project/models/savedNames.txt", "r")) as file:
        with (open(filePath+"savedNames.txt", "r")) as file:
            lines = file.readlines()
            if(lines):
                #print("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + lines[len(lines)-1].strip())
                #model.load_state_dict(torch.load("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + lines[len(lines)-1].strip(), weights_only=True))
                # Personal Computer Training
                #model.load_state_dict(torch.load("models/saves/" + lines[len(lines)-1].strip(), weights_only=True))
                model.load_state_dict(torch.load(filePath+"saves/"  + lines[len(lines)-1].strip(), weights_only=True))
    except IOError:
       print("Didnt Find Any Saved Models") 

    if(torch.cuda.is_available):
        model.to(torch.device("cuda"))
        
    #lossFunction = nn.CrossEntropyLoss()
    lossFunction = nn.BCEWithLogitsLoss()
    
    #Initializes a Adam W optimizer to be used in my training Loop

    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    
    #optimizer = torch.optim.SGD(model.parameters())
    #initialTime = time.time()
    fails = 0
    lastAccuracy = 1
    #mostAccurate = -1
    for epoch in range(epochs):
        print("Epoch: " + str(epoch))
        model.train()
        trainingLoss =trainingBlock(trainingLoader, model, optimizer, lossFunction, epoch)
        print("Trained")
        model.eval()
        accuracy = validationBlock(validationLoader, model, optimizer, lossFunction, epoch)
        
        print("Epoch: " + str(epoch+1) + "/"+ str(epochs) + " Training Loss: " + str(round(trainingLoss,5)) + " Accuracy: " + str(round(accuracy*100, 3)) + " %") 

        if(accuracy > 0.7):
            print("Accracy Above 70%. Setting Learning Rate To: 0.0005")
            for param_group in optimizer.param_groups:
                param_group['lr'] = 0.0005
        elif(accuracy > 0.9):
            print("Accracy Above 90%. Setting Learning Rate To: 0.0001")
            for param_group in optimizer.param_groups:
                param_group['lr'] = 0.0001

        if(lastAccuracy < accuracy):
            fails = fails+1
            print(fails)
            if(fails >= 10):
                print("Model No Longer Becoming More Accurate")
                break
        else:
            fails = 0
        lastAccuracy = accuracy
        print(f"Saving the model: ")
        # For my local machine
        #with open("models/savedNames.txt", "a") as file:
        
        #For a kaggle notebook
        #with open("/kaggle/working/Machine-Learning-Resume-Project/models/savedNames.txt", "a") as file:
        with open(filePath+"savedNames.txt", "a") as file:
            name = "model_" + (time.ctime(time.time()).replace(" ", "_").replace(":", "_"))
            file.write(name + "\n")
            # For running on my local machine
            #torch.save(model.state_dict(), ("models/saves/" + name))

            # For running on a kaggle notebook
            #torch.save(model.state_dict(), ("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + name))
            torch.save(model.state_dict(), (filePath+"saves/"+name))        
        
        #if((epoch+1 % 10 == 0) and (mostAccurate < accuracy)):
        #    print("Most Accurate Model Found Saving: " + str(accuracy))
        #    mostAccurate = accuracy
        #    torch.save(model, ("models/testingModelSave" + str(datetime.date().month) +":" + str(datetime.date().day) + ":" + str(time.time())))
            #Insert a save here
    #print((time.time()-initialTime))


def trainingBlock(trainingLoader, model, optimizer, lossFunction, epochIndex):

    device = torch.device("cuda")

    totalLoss = 0.0

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

    # Resseeding the transforms every time we train to avoid the model only learning to distinguish my exact training transforms  
    #random.seed(time.time())
   
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
            

