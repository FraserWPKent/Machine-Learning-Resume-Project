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
    def __init__(self, dataDirectory, transform=None):
        self.data = ImageFolder(dataDirectory, transform=transforms.Compose([
            transforms.Resize((224, 224), antialias=True), 
            transforms.ToTensor()
            ]))
        
        # Note: This mean will be an approximation based on the first sixth of the data. From my testing one sixth of the dataset seems to
        # give a good enough approximation of the true mean while also executing faste enough to be bearable. (Total time 12 seconds).
        # If training isint going well maybe modifying this fraction of dataset variable will help making the dataset better conditioned.
        print("Getting the list")
        fractionOfDataset = 6
        list = []
        for i in range(int(len(self.data)/fractionOfDataset)):
            list.append(self.data[i][0])
        #print("Stacking")
        image = torch.stack(list, dim=0)
        
        print("Calculating the mean and std")
        calcMean = image.mean(dim = (0,2,3))
        calcStd = image.std(dim=(0,2,3))
        
        #print("Calc Mean\n")
        #print(calcMean)
        #print("Calc Std\n")
        #print(calcStd)
        
        newTransform = transforms.Compose([
            transforms.Resize((224,224), antialias=True),
            transforms.ToTensor(),
            transforms.Normalize(mean=calcMean, std=calcStd)
        ])
        self.data.transform=newTransform   
        #timeEnd = time.time()
        #print("Total Time:" + str(timeEnd-timeStart))
        #print(timeEnd-timeStart)                  
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
print(im.__getitem__(19000))
#print(torch.version.cuda)
#print(torch.cuda.is_available())


#img = (im.getPilImage(1))
#img.show()