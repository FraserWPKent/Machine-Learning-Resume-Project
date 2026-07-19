import database as db
import modelArchitecturePractice as mp
import modelArchitecture as ma
import torch
import torch.nn as nn
import torchvision as vision
import training
from torch.utils.data import DataLoader



def main():
    # Initializing the Build Datasets
    trainingDataset = db.AiImageDetectorDataset("ImageDataset/Training", training=True)
    testingDataset = db.AiImageDetectorDataset("ImageDataset/Testing", training=False)

    #Placing the Datsets into a data loader
        # Batch size 128, with 8 workers has been the most efficient in terms of runtime for my computer
        # pin_memory included to optimize the process for my training
    trainingLoader = DataLoader(trainingDataset, shuffle=True, batch_size=128, num_workers=8, pin_memory=True)
    testingLoader = DataLoader(testingDataset, shuffle=False, batch_size=128, num_workers=8, pin_memory=True)
    #print(trainingDataset.__len__())
    #print(testingDataset.__len__())
    #print(testingDataset.classes)
    #temp = trainingDataset.__getitem__(100)
    # Temp 0 stores the tensor created from our image
    # Temp 1 stores the lable for the image
        # 0: Fake Faces, 1: Real Faces
    #print(temp[0])
    #print(temp[1])
    #temp2 = trainingDataset.__getitem__(12900)
    #print(temp2[1])

    #print(len(temp[0][0]))
    #print(len(temp[0][0][0]))

    training.trainingPrep(trainingLoader=trainingLoader, validationLoader=trainingLoader, epochs=5)


    #model.to(device)
    #batch = next(iter(trainingLoader))
    #features, labels = batch[0].to(device), batch[1].to(device)
    #print(labels)
    #print(model.forward(features))
    #print(model.parameters())





    #filter = [[[1,2,3],[4,5,6],[7, 8,9]]]
    #bias = [1]
    #convoluted = mp.ConvolutionManual(temp[0], bias, filter)
    #print(convoluted)
    #normalized = mp.BatchNormalize(convoluted[0], 0.5, 0.001)
    #print(normalized)
    #ReLUed = mp.ReLu(normalized)
    #print(ReLUed)

if __name__ == '__main__':
    main()