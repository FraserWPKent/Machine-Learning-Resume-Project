import torch
#import torch.nn as nn
from torch import nn

class ModelArch(nn.Module):
    def __init__(self):
        super().__init__()
        #self.conv = ((),(),())
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.batch = nn.BatchNorm2d(num_features=32)
        self.activation = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.linear = nn.Linear(32, 1)
        self.globalPool = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(p=0.2)

    def forward(self, x):
        
        x = self.conv1(x)
        #x = self.activation(x)
        #x = self.conv2(x)
        #x = self.activation(x)
        #x = self.conv3(x)
        x = self.batch(x)
        x = self.activation(x)
        x = self.pool(x)

        x = self.globalPool(x)
        x = torch.flatten(x, 1)
        x = self.linear(x)
        x = torch.squeeze(x)
        x = self.dropout(x)
        #print(x)
        #x = x.squeeze(1)
        return x
    
    def adjustSizes(self, inChannel, outChannel):
        self.conv = nn.Conv2d(in_channels = inChannel, out_channels=outChannel, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.batch = nn.BatchNorm2d(outChannel)



