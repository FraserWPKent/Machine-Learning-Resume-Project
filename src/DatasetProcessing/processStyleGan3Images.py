import os
import random
import cv2
import numpy as np
import time

def main():
    backgroundList = os.listdir("src/DatasetProcessing/BackgroundImages")
    styleGanImages = os.listdir("src/DatasetProcessing/PreProcessingStyleGanFullBodies")

    filePath = "src/DatasetProcessing/StyleGanImagesWithBackgrounds"
    oldImages = os.listdir(filePath)

    for fileName in oldImages:
        #print(filePath+"/"+fileName)
        #time.sleep(1)
        if(os.path.exists(filePath+"/"+fileName)):
            print("Old Image Exists Removing It")
            os.remove(filePath+"/"+fileName)

    #time.sleep(10)

    total =0 
    #for x in range(0, 100):
    for fileName in styleGanImages:
        #fileName = styleGanImages[x]
        index = random.randint(0, backgroundList.__len__()-1)
        #print("Image to be processed: " + fileName)
        #print("Background to be added: " + backgroundList[index])

        background = cv2.imread("src/DatasetProcessing/BackgroundImages/" + backgroundList[index], cv2.IMREAD_COLOR)
        foreground = cv2.imread("src/DatasetProcessing/PreProcessingStyleGanFullBodies/" + fileName, cv2.IMREAD_COLOR)

        #print(background.shape)
        #print(foreground.shape)

        
            #cv2.imshow("Image", foreground)
            #cv2.waitKey(2)

        #time.sleep(3)        
        h,w,c = foreground.shape
        rgbThreshold = 200

        white_mask = cv2.inRange(foreground, np.array([rgbThreshold, rgbThreshold, rgbThreshold], dtype="uint8"), np.array([255, 255, 255], dtype="uint8"))
            #distance = np.max(255 - foreground, axis=2)
            #mask = np.where(distance > 20, 255, 0).astype(np.uint8)

        flooding_mask = np.zeros((h+2, w+2), np.uint8)

        flood = white_mask.copy()

        cv2.floodFill(flood, flooding_mask, (0, 0), 255)
        cv2.floodFill(flood, flooding_mask, (foreground.shape[1] - 1, 0), 255)
        cv2.floodFill(flood, flooding_mask, (0, foreground.shape[0] - 1), 255)
        cv2.floodFill(flood, flooding_mask,(foreground.shape[1] - 1, foreground.shape[0] - 1),255)


        
        finalHeight = int(h/4)
        widthCenter = int(w/2)
        widthOffset = int(w/4)

        resizedFlood = flood[0:(finalHeight), widthCenter-widthOffset:widthCenter+widthOffset]

        newHeight, newWidth = resizedFlood.shape

        #Getting a percentage of the image that is dark to roughtly weed out all of the stylegan 3 images that have white clothes getting masked out
        darkPixels = 0
        for i in range(0, newHeight):
            for j in range(0, newWidth):
                if(resizedFlood[i][j] == 0):
                    darkPixels += 1

        percentage = darkPixels/(newHeight*newWidth)
        print(percentage)

        #If to much of the image is white dont save it        
        if(percentage < 0.35):
            continue

        alpha = cv2.bitwise_not(flood)
        alpha = alpha.astype(np.float32)/255.0
        alpha = alpha[:,:,np.newaxis]
        

        resizedBackground = background[0:(2*h),0:(2*w)]
        resizedBackground = cv2.resize(resizedBackground, (w, h), interpolation=cv2.INTER_AREA)

        


            #cv2.imshow("Foreground", foreground)
            #cv2.imshow("Background", resizedBackground)
        #cv2.imshow("Mask", flood)

        #key =cv2.waitKey(0)

        #if(key == 100):
        #    exit()



            #cv2.imshow("Alpha", (alpha * 255).astype(np.uint8))

            #cv2.waitKey(0)

        

        dest = (resizedBackground.astype(np.float32)*(1-alpha) + foreground.astype(np.float32)*alpha)
        dest = np.clip(dest, 0, 255).astype(np.uint8)

        #destShape = dest.shape

        #height = int(destShape[0]/2.5)
        #widthCenter = int(destShape[1]/2)
        #widthOffset = int(destShape[1]/4)

        dest = dest[0:(finalHeight), widthCenter-widthOffset:widthCenter+widthOffset]

        


        initialRow = widthCenter-widthOffset

        if (True):
            #cv2.imshow("Image", dest)
            #key = cv2.waitKey(0)
            #print(key)
            #if (key == 113):
            #    exit()
            total = total+1
            print("Saving: " + fileName)
            cv2.imwrite("src/DatasetProcessing/StyleGanImagesWithBackgrounds/WBG" + fileName, dest)
        

    print("Useable Images: " + str(total))
    cv2.destroyAllWindows()
        #time.sleep(3)


if (__name__ == "__main__"):
    main()