import torch
import modelArchitecture as ma
import torch.nn as nn
import time
import datetime



def trainingPrep(trainingLoader, validationLoader, epochs):
    

    model = ma.ModelArch()
    model.to(torch.device("cuda"))
    #lossFunction = nn.CrossEntropyLoss()
    lossFunction = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters())
    initialTime = time.time()
    fails = 0
    lastAccuracy = 1
    mostAccurate = 1
    for epoch in range(epochs):
        print("Epoch: " + str(epoch))
        model.train()
        trainingLoss =trainingBlock(trainingLoader, model, optimizer, lossFunction, epoch)
        print("Trained")
        model.eval()
        accuracy = validationBlock(validationLoader, model, optimizer, lossFunction, epoch)
        
        print("Epoch: " + str(epoch+1) + "/"+ str(epochs) + " Training Loss: " + str(trainingLoss) + " Accuracy: " + str((accuracy*100)) + " %") 
    
        if(lastAccuracy < accuracy):
            fails = fails+1
            print(fails)
            if(fails >= 5):
                print("Model No Longer Becoming More Accurate")
                break
        else:
            fails = 0
        
        if((epoch+1 % 10 == 0) and (mostAccurate > accuracy)):
            print("Most Accurate Model Found Saving: " + str(accuracy))
            mostAccurate = accuracy
            torch.save(model, ("models/testingModelSave" + str(datetime.date().month) +":" + str(datetime.date().day) + ":" + str(time.time())))
            #Insert a save here
    print((time.time()-initialTime))


def trainingBlock(trainingLoader, model, optimizer, lossFunction, epochIndex):
    device = torch.device("cuda")
    totalLoss = 0.0
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
        #print(x)
        #print(i)
        #x = x+32
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
    device = torch.device("cuda")
    loss = 0.0
    total = 0
    with torch.no_grad():
        for i, data in enumerate(validationLoader):
            items, labels = data[0].to(device), data[1].float().to(device)

            outputs = model(items)

            #print(len(outputs))
            
            #TODO: FIGURE OUT WHY I CANNOT GET THIS TO TURN INTO A NORMAL NUMBER
            total += torch.argmax(outputs).float()
            print(total)
            #print(predictions)
            #for p in range(len(predictions)):
                #print(predictions[p])

            #currentLoss = lossFunction(outputs, labels)
            
            #loss += currentLoss.item()
        
        return total.float()/(len(validationLoader))
            

