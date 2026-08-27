import torch
import modelArchitecture as ma
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import time
import datetime
import torchvision.transforms as transforms
import random



def trainingPrep(trainingLoader, validationLoader, epochs):
    model = ma.ModelArch()
    try:
        #For running on my local machine
        #with (open("models/savedNames.txt", "r")) as file:
        #For running on the kaggle notebook
        with (open("/kaggle/working/Machine-Learning-Resume-Project/models/savedNames.txt", "r")) as file:
            lines = file.readlines()
            if(lines):
                print("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + lines[len(lines)-1].strip())
                model.load_state_dict(torch.load("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + lines[len(lines)-1].strip(), weights_only=True))
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
        with open("/kaggle/working/Machine-Learning-Resume-Project/models/savedNames.txt", "a") as file:
            name = "model_" + (time.ctime(time.time()).replace(" ", "_").replace(":", "_"))
            file.write(name + "\n")
            # For running on my local machine
            #torch.save(model.state_dict(), ("models/saves/" + name))

            # For running on a kaggle notebook
            torch.save(model.state_dict(), ("/kaggle/working/Machine-Learning-Resume-Project/models/saves/" + name))        
        
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
    # TODO: FIGURE OUT WHY THIS IS PRODUCING PIL IMAGES INSTEAD OF TENSORS EVEN THOUGH IM APPLYING TO TENSOR TO IT
    # JULY 20TH figure this out soon
    # myTransform = [
    #         transforms.Resize((224, 224), antialias=True), 
    #         transforms.GaussianBlur(3, [random.randint(25, 40)/100.0, random.randint(50, 65)/100.0]),
    #         transforms.ToTensor(),
    #         transforms.Normalize(mean=[0.5215, 0.4260, 0.3793], std=[0.2747, 0.2478, 0.2481]),
    #         #transforms introduced to simulate real world image irregularities that could come into effect when an image is posted to the internet
    #         # Current transformations:
    #             # 50 50 flip. Avoids over relying on specific framing that arise in real world photography and ai image generation
    #         transforms.RandomHorizontalFlip(0.5),
    #             # Adding some random blurring to the photographs to simulate problems created by repeated reposting, bad data transfers, etc...
            
    #             #Introduce cropping algoritms tommorow.
    #         #transforms.FiveCrop
    #     ]
    # trainingLoader.dataset.transform = transforms.Compose(myTransform)
    #lastLoss=0.0
    itemsProcessed = len(trainingLoader)
    x = 0
    startTime = time.time()
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

            #TODO: FIGURE OUT HOW TO CALCULATE AVERAGES HERE
            #waste,predicted = torch.max(outputs, 0)
            #for x in range(predicted.size()):
            #    if(predicted[x].item() == labels[x].item()):
            #        print("Correct")
            #        total +=1
            total += (predictions==labels.float().view(-1)).sum().item()
            #print(total)
        print(total)
        print(len(validationLoader.dataset))
        return total/(len(validationLoader.dataset))
            

