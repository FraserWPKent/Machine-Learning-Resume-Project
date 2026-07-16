import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
import torchvision as vision
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
from torchvision.transforms import functional
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
import time


class AiImageDetectorDataset(Dataset):
    def __init__(self, dataDirectory, transform=None, training=True):
        myTransform = [
            transforms.Resize((224, 224), antialias=True), 
            transforms.RandomHorizontalFlip(0.5),
            transforms.ToTensor()
        ]
        if(training):
            myTransform.append(transforms.Normalize(mean=[0.5215, 0.4260, 0.3793], std=[0.2747, 0.2478, 0.2481]))
        self.data = ImageFolder(dataDirectory, transform=transforms.Compose(myTransform))
        
        ### CODE FOR FINDING THE MEAN AND STD OF A SET OF VALUES. STAYING HERE IN CASE I NEED TO USE IT AGAIN AFTER A DATASET CHANGE
        # print("Getting the list")
        # fractionOfDataset = 1
        # list = []
        # for i in range(int(len(self.data)/fractionOfDataset)):
        #     list.append(self.data[i][0])
        # image = torch.stack(list, dim=0)
        
        # print("Calculating the mean and std")
        # calcMean = image.mean(dim = (0,2,3))
        # calcStd = image.std(dim=(0,2,3))
        
        # print("Calc Mean\n")
        # print(calcMean)
        # print("Calc Std\n")
        # print(calcStd)
                   
        # Setup the data

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index] 


    @property
    def classes(self):
        return self.data.classes


# This method will be a practice implementation of image convolution for learning sake. I have no intention of actually using this as the
# the built in nn.conv2d is simply better than anything I can make on my own as a student.
def ConvolutionManual():
    print("Manual Convolution")

    



trainingDataset = AiImageDetectorDataset("ImageDataset/Training", training=True)
testingDataset = AiImageDetectorDataset("ImageDataset/Testing", training=False)
trainingLoader = DataLoader(trainingDataset, shuffle=True, batch_size=32)
testingLoader = DataLoader(testingDataset, shuffle=False, batch_size=32)
print(trainingDataset.__len__())
print(testingDataset.__len__())
print(testingDataset.classes)
temp = trainingDataset.__getitem__(100)
# Temp 0 stores the tensor created from our image
# Temp 1 stores the lable for the image
    # 0: Fake Faces, 1: Real Faces
print(temp[0])
print(temp[1])
temp2 = trainingDataset.__getitem__(12900)
print(temp2[1])

#print(torch.version.cuda)
#print(torch.cuda.is_available())
