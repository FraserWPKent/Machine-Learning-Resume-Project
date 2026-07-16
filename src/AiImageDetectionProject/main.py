import database as db
import modelArchitecturePractice as mp
import torch
import torchvision as vision
from torch.utils.data import DataLoader

trainingDataset = db.AiImageDetectorDataset("ImageDataset/Training", training=True)
testingDataset = db.AiImageDetectorDataset("ImageDataset/Testing", training=False)

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

print(len(temp[0][0]))
print(len(temp[0][0][0]))

filter = [[[1,2,3],[4,5,6],[7, 8,9]]]
bias = [1]
convoluted = mp.ConvolutionManual(temp[0], bias, filter)
print(convoluted)
normalized = mp.BatchNormalize(convoluted[0], 0.5, 0.001)
print(normalized)
ReLUed = mp.ReLu(normalized)
print(ReLUed)