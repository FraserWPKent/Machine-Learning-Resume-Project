import torch
import math



# This method will be a practice implementation of image convolution for learning sake. I have no intention of actually using this as the
# the built in nn.conv2d is simply better than anything I can make on my own as a student.
# For each filter layer this program should 
def ConvolutionManual(tensor, bias, filters):
    resultTensor = torch.zeros(len(filters),len(tensor[0]), (len(tensor[0][0]))) 
    for k in range(len(filters)):
        if(len(tensor) == 0 or len(tensor[0]) == 0 or len(tensor[0][0]) == 0):
            return [[[]]]
        for y in range(len(tensor[0])):
            for x in range(len(tensor[0][y])):
                weightedSum = 0 
                xOffset = -1
                yOffset = -1
                for xOffset in range(-1, 2):
                    for yOffset in range(-1, 2):
                        if((x+xOffset < 0 or y+yOffset < 0) or x+xOffset >= len(tensor[0]) or y+yOffset >= len(tensor[0])):
                            weightedSum += 0
                        else:
                            weightedSum += (tensor[0][y+yOffset][x+xOffset]+tensor[1][y+yOffset][x+xOffset]+tensor[2][y+yOffset][x+xOffset])*(filters[k][yOffset+1][xOffset+1])
                resultTensor[k][y][x] = weightedSum + bias[k] 
    return resultTensor

def getMean(tensor):
    total = 0
    for y in range(len(tensor)):
        for x in range(len(tensor[0])):
            total += tensor[y][x]

    return math.floor(total/(len(tensor) * len(tensor[0])))
def getStd(tensor, mean):
    std = 0
    for y in range(len(tensor)):
        for x in range(len(tensor[y])):
            std+=(tensor[y][x]-mean)**2
    std /= len(tensor)
    return std

def BatchNormalize(tensor, gamma, beta):
    mean = getMean(tensor)
    std = getStd(tensor, mean)
    epsilon = (10 ** -5)
    for y in range(len(tensor)):
        for x in range(len(tensor[y])):
            tensor[y][x] = gamma*((tensor[y][x]-mean)/(math.sqrt(std+epsilon)))+ beta
        
    return tensor

def ReLu(tensor):
    for y in range(len(tensor)):
        for x in range(len(tensor[0])):
            tensor[y][x] = max(0, tensor[y][x])

    return tensor
                     