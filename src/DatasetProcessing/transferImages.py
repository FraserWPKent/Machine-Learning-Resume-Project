import os
import shutil
import random


def main():
    diffusionDirs = os.listdir("src/DatasetProcessing/arc2face-4")
    kaggleStyleGanImages = os.listdir("src/DatasetProcessing/StyleGan3KaggleFaces")
    styleGanHumanImages = os.listdir("src/DatasetProcessing/StyleGanImagesWithBackgrounds")

    #Moving the Diffusion Directory
    total = 0
    #getting the cutoff points for moving values into my testing, training, and validation data blocks
    seventyPercent = int(len(diffusionDirs) * 0.7)
    eightyFivePercent = int(len(diffusionDirs) * 0.85)

    # randomly shuffling the diffusionDirs because the data is currently sorted based on general features (age, race, etc) and
    # I want my model to have a good range of types of data when training and testing
    for index in range(len(diffusionDirs)-1, 0,-1):
        #Bad data locality but for arrays this small it shoudnt have that much of an effect
        randIndex = random.randint(0, index+1)
        #print("Swaping: " + str(index) + " and " + str(randIndex))
        temp = diffusionDirs[index]
        diffusionDirs[index] = diffusionDirs[randIndex]
        diffusionDirs[randIndex] = temp

    
    for dir in diffusionDirs:
        tempInnerDir = os.listdir("src/DatasetProcessing/arc2face-4/"+dir)
        #Randomly choose one of the generated images. 
        #currently only choosing one of the images for each "person" but I can increase this if I want to raise the number 
        # of diffusion based images in my dataset
        for i in range(0, 1):
            randIndex = random.randint(0, len(tempInnerDir)-1)
            currentImage = tempInnerDir[randIndex]
            print("Total: " + str(total))
            if(total <= seventyPercent):
                shutil.copy("src/DatasetProcessing/arc2face-4/"+dir+"/"+currentImage, "ImageDataset/Training/Fake Faces")
            elif(total <= eightyFivePercent):
                shutil.copy("src/DatasetProcessing/arc2face-4/"+dir+"/"+currentImage, "ImageDataset/Testing/Fake Faces")
            else:
                shutil.copy("src/DatasetProcessing/arc2face-4/"+dir+"/"+currentImage, "ImageDataset/Validate/Fake Faces")
            total += 1

    #Moving the kaggle style gan database
    total = 0
    #getting the cutoff points for moving values into my testing, training, and validation data blocks
    seventyPercent = int(len(kaggleStyleGanImages) * 0.7)
    eightyFivePercent = int(len(kaggleStyleGanImages) * 0.85)

    # randomly shuffling the kaggleStyleGanImages to ensure that if there is some uninteded order of elements in the directory
    # it doesnt effect the characteristics my model is trained, tested, and validated on.
    for index in range(len(kaggleStyleGanImages)-1, 0,-1):
        #Bad data locality but for arrays this small it shoudnt have that much of an effect
        randIndex = random.randint(0, index+1)
        #print("Swaping: " + str(index) + " and " + str(randIndex))
        temp = kaggleStyleGanImages[index]
        kaggleStyleGanImages[index] = kaggleStyleGanImages[randIndex]
        kaggleStyleGanImages[randIndex] = temp

    #for i in range(0, 3):
    for currentImage in kaggleStyleGanImages:
        #currentImage = kaggleStyleGanImages[i]
        #Randomly choose one of the generated images. 
        #currently only choosing one of the images for each "person" but I can increase this if I want to raise the number 
        # of diffusion based images in my dataset
        print("Total: " + str(total))
        if(total <= seventyPercent):
            shutil.copy("src/DatasetProcessing/StyleGan3KaggleFaces/"+currentImage, "ImageDataset/Training/Fake Faces")
        elif(total <= eightyFivePercent):
            shutil.copy("src/DatasetProcessing/StyleGan3KaggleFaces/"+currentImage, "ImageDataset/Testing/Fake Faces")
        else:
            shutil.copy("src/DatasetProcessing/StyleGan3KaggleFaces/"+currentImage, "ImageDataset/Validate/Fake Faces")
        total += 1

    #Moving the self generated style gan human database
    total = 0
    #getting the cutoff points for moving values into my testing, training, and validation data blocks
    seventyPercent = int(len(styleGanHumanImages) * 0.7)
    eightyFivePercent = int(len(styleGanHumanImages) * 0.85)

    # randomly shuffling the styleGanHumanImages to ensure that if there is some uninteded order of elements in the directory
    # it doesnt effect the characteristics my model is trained, tested, and validated on.
    for index in range(len(styleGanHumanImages)-1, 0,-1):
        #Bad data locality but for arrays this small it shoudnt have that much of an effect
        randIndex = random.randint(0, index+1)
        #print("Swaping: " + str(index) + " and " + str(randIndex))
        temp = styleGanHumanImages[index]
        styleGanHumanImages[index] = styleGanHumanImages[randIndex]
        styleGanHumanImages[randIndex] = temp

    #for i in range(0, 3):
    for currentImage in styleGanHumanImages:
        #currentImage = styleGanHumanImages[i]
        #Randomly choose one of the generated images. 
        #currently only choosing one of the images for each "person" but I can increase this if I want to raise the number 
        # of diffusion based images in my dataset
        print("Total: " + str(total))
        if(total <= seventyPercent):
            shutil.copy("src/DatasetProcessing/StyleGanImagesWithBackgrounds/"+currentImage, "ImageDataset/Training/Fake Faces")
        elif(total <= eightyFivePercent):
            shutil.copy("src/DatasetProcessing/StyleGanImagesWithBackgrounds/"+currentImage, "ImageDataset/Testing/Fake Faces")
        else:
            shutil.copy("src/DatasetProcessing/StyleGanImagesWithBackgrounds/"+currentImage, "ImageDataset/Validate/Fake Faces")
        total += 1



if(__name__ == "__main__"):
    main()


