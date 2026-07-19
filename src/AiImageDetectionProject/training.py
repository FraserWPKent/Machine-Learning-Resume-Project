import torch
import modelArchitecture as ma
import torch.nn as nn
import time



def trainingLoop(trainingLoader, validationLoader):
    

    model = ma.ModelArch()
    model.to(torch.device("cuda"))
    #lossFunction = nn.CrossEntropyLoss()
    lossFunction = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters())
    for epoch in range(5):
        print("Epoch: " + str(epoch))
        model.train()
        lastLoss =trainingBlock(trainingLoader, validationLoader, model, optimizer, lossFunction, epoch)
        model.eval()
        print(lastLoss)
    



def trainingBlock(trainingLoader, validationLoader, model, optimizer, lossFunction, epochIndex):
    device = torch.device("cuda")
    runningLoss = 0.
    lastLoss=0.
    #x = 0
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
        runningLoss += loss.item()
        if i % 100 == 0:
            lastLoss = runningLoss / 100 # loss per batch
            print(f'  batch {i + 1} loss: {lastLoss}')
            #tb_x = epochIndex * len(trainingLoader) + i + 1
            #tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            runningLoss = 0.

    print(time.time()-startTime)
    return lastLoss