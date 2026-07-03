import cv2
import numpy
import random

#for i in range(1,44):
for i in range(1, 5):
    currentPath = "TestingImageDataSet\\Gemini\\"+str(i)+".png"
    #print(currentPath)
    currentImage = cv2.imread(currentPath)
    resized = cv2.resize(currentImage, (224, 224))


    #noisyImage = None
    #if(random()%5 == 0):
    guaNoise = numpy.random.normal(0, 15, resized.shape).astype(numpy.uint8)
    guaNoisyImage = cv2.add(resized, guaNoise)

    noisy_image = resized.copy()
    randNoise = numpy.random.randint(-25, 25 + 1, noisy_image.shape)
    randNoisyImage = numpy.clip(noisy_image + randNoise, 0, 255).astype(numpy.uint8)
    blurredImage = cv2.blur(resized, (3,3));
    #resizedGray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    laplacianImage = cv2.Laplacian(resized, cv2.CV_16S, ksize=7)
    #elif(random()%5 == 0):

    resizedNormalized = resized.astype(float)/255.0
    guaNoisyNormalized = guaNoisyImage.astype(float)/255.0
    randNoisyNormalized = randNoisyImage.astype(float)/255.0
    blurredNormalized = blurredImage.astype(float)/255.0

    cv2.imshow("Original Normalized",resizedNormalized)
    cv2.imshow("Noisy Normalized", guaNoisyNormalized)
    cv2.imshow("Rand Noise Normalized", randNoisyNormalized)
    cv2.imshow("Blurred" , blurredNormalized)
    cv2.imshow("Laplacian: ", laplacianImage)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()


    #print(resizedNormalized.dtype)   
    #print(resizedNormalized.min)
    #print(resizedNormalized.max)

#cv2.imwrite("NormalizedImages\\Gemini\\1_resizedNormalized.png", resizedNormalized.astype(numpy.uint16))
#cv2.imwrite("NormalizedImages\\Gemini\\1_noisyNormalized.png", noisyNormalized.astype(numpy.uint16))


#resizedNormPartOne = (resized.astype(float))

#resizedNormPartTwo = (resized.astype(float)-0.5)/0.5
#gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#normalized_color_image = cv2.normalize(resized, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
#normalized_color_image = cv2.cvtColor(normalized_gray_image, cv2.COLOR_GRAY2BGR)

#cv2.imshow("Original",resized)
#cv2.imshow("Original Normalized",resizedNormalized)
#if(noisyImage != None):
#cv2.imshow("Noisy", noisyImage)
#cv2.imshow("Noisy Normalized", noisyNormalized)
#cv2.imshow("Part 2",resizedNormPartTwo)
#cv2.imshow("Gray",normalized_color_image)
#cv2.waitKey(100000)

