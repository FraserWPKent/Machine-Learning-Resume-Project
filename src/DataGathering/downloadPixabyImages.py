import requests
import time
import random
import os
import sys

def main():
    if(len(sys.argv) < 2):
        print("Please provide a txt file to read out of")
        sys.exit()

    length = 0
    with open(sys.argv[1]) as file:
        for line in file:
            length+=1
        file.close()

    print(length)

    with open(sys.argv[1]) as inputFile:
        with open("/kaggle/working/Machine-Learning-Resume-Project/src/DatasetProcessing/PixabyImages/downloadedIDs.txt", "a") as outputFile:
            
            numberOfBadResponses = 0
            rand = random.Random()

            minimumWait = 3.7
            i = 0
            ids= []

            with open("/kaggle/working/Machine-Learning-Resume-Project/src/DatasetProcessing/PixabyImages/downloadedIDs.txt") as temp:
                for line in temp:
                    ids.append(int(line.strip()))

            print(ids)
            numberOfImages = len(ids)
            for url in inputFile:
                if(((i+1)) % 120 == 0):
                    time.sleep(300 + rand.random()*60)
                elif(((i+1)) % 80 == 0):
                    time.sleep(120 + rand.random()*30)

                if(i > 24):
                    sys.exit()
                
                # Getting the current images's id and then skipping the Tags, and Main URL
                if(i % 4 == 0):
                    #Skipping this image if its already been downloaded
                    if((int(url[4:len(url)].strip()) in ids)):
                        i+=4
                        next(inputFile, None)
                        next(inputFile, None)
                        next(inputFile, None)
                        continue
                    ids.append(int(url[4:len(url)].strip()))
                    print(ids[len(ids)-1])
                    i+=1
                elif(i % 4 == 1 or i % 4 == 2):
                    i+=1
                    continue
                else:
                    i+=1
                    url = url[19:len(url)].strip()
                    print(url)
                    #sys.exit()
                    reqResponse = requests.get(url)

                    if(reqResponse.status_code == 403 or reqResponse.status_code == 401 or reqResponse.status_code == 404):
                        print("Pixaby Responding With Forbidden, Unauthorized, or Not Found. Shutting Down")
                        print(reqResponse.status_code)
                        print(reqResponse.text)
                        sys.exit()
                    elif(reqResponse.status_code == 429):
                        print("Making To Many Requests Too Quickly")
                        minimumWait *= 2.1
                        numberOfBadResponses += 1
                        time.sleep(minimumWait + rand.random()*10.3)
                    elif(reqResponse.status_code != 200):
                        if(numberOfBadResponses == 10):
                            print("Got too many bad responses shutting down")
                            print(reqResponse.text)
                            sys.exit()
                        else:
                            print("Error code: " + str(reqResponse.status_code))
                            print(str(reqResponse.text))
                            time.sleep(minimumWait + rand.random()*10.2)
                    imgData = reqResponse.content

                    with open("/kaggle/working/Machine-Learning-Resume-Project/src/DatasetProcessing/PixabyImages/Real/pix_real_image_" + str(numberOfImages) + ".jpg", "wb") as image:
                        image.write(imgData)
                        numberOfImages += 1
                        outputFile.write(str(ids[len(ids)-1]) + "\n")
                    time.sleep(minimumWait + rand.random()*5.0)

if(__name__=="__main__"):
    main()