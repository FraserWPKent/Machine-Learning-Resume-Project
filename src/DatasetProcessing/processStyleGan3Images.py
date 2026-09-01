import os
import random
import cv2
import numpy as np

def main():
    backgroundList = os.listdir("src\DatasetProcessing\BackgroundImages")
    styleGanImages = os.listdir("src\DatasetProcessing\PreProcessingStyleGanFullBodies")

    for fileName in styleGanImages:
        index = random.randint(0, backgroundList.__len__()-1)
        print("Image to be processed: " + fileName)
        print("Background to be added: " + backgroundList[index])

        background = cv2.imread("src/DatasetProcessing/BackgroundImages/" + backgroundList[index])
        foreground = cv2.imread("src/DatasetProcessing/PreProcessingStyleGanFullBodies/" + fileName)

        if(fileName == styleGanImages[0]):
            cv2.imshow("Image", foreground)
            cv2.waitKey(5)


if (__name__ == "__main__"):
    main()