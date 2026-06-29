import cv2
import numpy

#for i in range(1,38):
currentPath = "ImageDataSet\\Gemini\\"+str(1)+".png"
print(currentPath)
currentImage = cv2.imread(currentPath)
resized = cv2.resize(currentImage, (224, 224))
resizedNormPartOne = resized.astype(float)/255.0
#resizedNormPartTwo = (resized.astype(float)-0.5)/0.5
#gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#normalized_color_image = cv2.normalize(resized, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
#normalized_color_image = cv2.cvtColor(normalized_gray_image, cv2.COLOR_GRAY2BGR)

cv2.imshow("Original",resized)
cv2.imshow("Part 1",resizedNormPartOne)
#cv2.imshow("Part 2",resizedNormPartTwo)
#cv2.imshow("Gray",normalized_color_image)
cv2.waitKey(10000)
cv2.destroyAllWindows()
