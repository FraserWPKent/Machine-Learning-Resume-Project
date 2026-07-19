import torch
import modelArchitecture as ma
import torch.nn as nn
import time



def trainingPrep(trainingLoader, validationLoader, epochs):
    

    model = ma.ModelArch()
    model.to(torch.device("cuda"))
    #lossFunction = nn.CrossEntropyLoss()
    lossFunction = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters())
    for epoch in range(epochs):
        #print("Epoch: " + str(epoch))
        model.train()
        trainingLoss =trainingBlock(trainingLoader, model, optimizer, lossFunction, epoch)
        model.eval()
        accuracy = validationBlock(validationLoader, model, optimizer, lossFunction, epoch)
        print("Epoch: " + str(epoch+1) + "/"+ str(epochs) + " Training Loss: " + str(trainingLoss) + " Accuracy: " + str(round((1-accuracy)*100, 5)) + " %") 
    



def trainingBlock(trainingLoader, model, optimizer, lossFunction, epochIndex):
    device = torch.device("cuda")
    runningLoss = 0.0
    lastLoss=0.0
    itemsProcessed = len(trainingLoader)
    x = 0
    #startTime = time.time()
    for i, data in enumerate(trainingLoader):
        items, labels = data[0].to(device), data[1].float().to(device)
        optimizer.zero_grad()


        outputs = model(items)

        loss = lossFunction(outputs, labels)
        loss.backward()

        optimizer.step()
        #print(x)
        #print(i)
        #x = x+32
        runningLoss += loss.item()
        if (i+1) % 25 == 0:
            lastLoss = runningLoss / 25 # loss per batch
            print(f'  batch {i + 1} loss: {lastLoss}')
            #tb_x = epochIndex * len(trainingLoader) + i + 1
            #tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            runningLoss = 0.0
            x=0
            #itemsProcessed -= x

    #print(time.time()-startTime)
    return lastLoss

def validationBlock(validationLoader, model, optimizer, lossFunction, epochIndex):
    device = torch.device("cuda")
    loss = 0.0
    with torch.no_grad():
        for i, data in enumerate(validationLoader):
            items, labels = data[0].to(device), data[1].float().to(device)

            outputs = model(items)

            currentLoss = lossFunction(outputs, labels)
            
            loss += currentLoss.item()
        
        return loss/(len(validationLoader))
            

