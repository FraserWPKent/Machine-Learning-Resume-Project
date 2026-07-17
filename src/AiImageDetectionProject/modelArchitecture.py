import torch
#import torch.nn as nn
from torch import nn

class ModelArch(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.batch = nn.BatchNorm2d(num_features=32)
        self.activation = nn.ReLU()
        self.pool = nn.MaxPool2d(2)

    def forward(self, x):
        x = self.conv(x)
        x = self.batch(x)
        x = self.activation(x)
        x = self.pool(x)
        return x
    
    def adjustSizes(self, inChannel, outChannel):
        self.conv = nn.Conv2d(in_channels = inChannel, out_channels=outChannel, kernel_size=3, stride=1, padding=1, padding_mode="zeros")
        self.batch = nn.BatchNorm2d(outChannel)



