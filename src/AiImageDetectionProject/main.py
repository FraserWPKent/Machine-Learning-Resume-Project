import database as db
import modelArchitecturePractice as mp
import modelArchitecture as ma
import torch
import torch.nn as nn
import torchvision as vision
import training
from torch.utils.data import DataLoader
import sys


def main():
    if(sys.argv.__len__() != 3):
        print("Not Enough Arguments")
        sys.exit()

    if(int(sys.argv[2])):
        # Initializing the Build Datasets when working on kaggle
        trainingDataset = db.AiImageDetectorDataset("/kaggle/input/datasets/williamkent1234321/updated-ai-image-detected-dataset/Training", training=True)
        testingDataset = db.AiImageDetectorDataset("/kaggle/input/datasets/williamkent1234321/updated-ai-image-detected-dataset/Validate", training=False)
        trainingLoader = DataLoader(trainingDataset, shuffle=True, batch_size=128, num_workers=4, pin_memory=True)
        testingLoader = DataLoader(testingDataset, shuffle=False, batch_size=128, num_workers=4, pin_memory=True)
    else:
        #Initializing the Build Datasets when working on my personal machine
        trainingDataset = db.AiImageDetectorDataset("ImageDataset/Training", training=True)
        testingDataset = db.AiImageDetectorDataset("ImageDataset/Validate", training=False)
        trainingLoader = DataLoader(trainingDataset, shuffle=True, batch_size=128, num_workers=8, pin_memory=True)
        testingLoader = DataLoader(testingDataset, shuffle=False, batch_size=128, num_workers=8, pin_memory=True)
    
    training.trainingPrep(trainingLoader=trainingLoader, validationLoader=testingLoader, epochs=int(sys.argv[1]), tag=int(sys.argv[2]))

if __name__ == '__main__':
    main()