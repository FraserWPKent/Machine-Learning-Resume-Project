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



class AiImageDetectorDataset(Dataset):
    def __init__(self, dataDirectory, transform=None):
        self.data = ImageFolder(dataDirectory, transform=transforms.Compose([
            transforms.Resize((224, 224), antialias=True), 
            transforms.ToTensor()
            ]))
        
        #TODO: Optimize this code for finding the mean and std of my dataset. It takes too long for my liking
        print("getting the list")
        list = []
        for i in range(len(self.data)):
            list.append(self.data[i][0])
        print("Stacking")
        image = torch.stack(list, dim=0)
        print("Calculating the mean and std")
        calcMean = image.mean(dim = (0,2,3))
        calcStd = image.std(dim=(0,2,3))
        #print(calcMean)
        #print(calcStd)
        newTransform = transforms.Compose([
            transforms.Resize((224,224), antialias=True),
            transforms.ToTensor(),
            transforms.Normalize(mean=calcMean, std=calcStd)
        ])
        self.data.transform=newTransform                     
        # Setup the data

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]    

        @property
        def classes(self):
            return self.data.classes


im = AiImageDetectorDataset("ImageDataSet/archive")
print(im.__len__())
print(im.__getitem__(1))
#print(torch.version.cuda)
#print(torch.cuda.is_available())


#img = (im.getPilImage(1))
#img.show()