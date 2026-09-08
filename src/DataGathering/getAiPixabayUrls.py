import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
import os
import sys
import time
import random

import requests





def testngSelenium():
    print("DONT BREAK STUFF")
        #options = Options()
    
        #options.add_argument("-headless")
        #options.add_argument("-private")
        #options.add_argument("-profile=C:/Users/fwpke/AppData/Roaming/Mozilla/Firefox/Profiles/7DqtqHHk.Profile 1")
    
        #driver = webdriver.Firefox(options=options)
    
        #driver.get("https://google.com/")
    
        #randGenerator = random.Random()
        #currentTime = int(time.time())
        #randGenerator.seed(currentTime)
        #waitTime = randGenerator.random()*5
        #print(currentTime)
        #print(waitTime)
        #time.sleep(10)  
        #print("Ending")
        #driver.implicitly_wait(30)
          
        #title = driver.title
        #print(title)
    
        #driver.quit()

def requestImageURLS(numReqs, file, tags, unacceptableWords, curPage, key, ids):
    totalAccepted = 0
    endPage = curPage+numReqs
    #print("Getting Images For " + coreTag)
    for i in range(curPage, endPage):
        print("Page: " + str(i))
        # constructing the rest api url
        
        url = "https://pixabay.com/api/?key=" + key + "&q=" + tags[0]
        for x in range(1, len(tags)):
                url += "+" + tags[x]
        url += "&image_type=photo&page="+str(i+1)+"&per_page=100&safesearch=true&category=people"
        req = requests.get(url=url)
        if (req.status_code != 200):
            print("Failed Request. Status Code: " + str(req.status_code))
            # If Im Overdoing it on the api requests wait for a bit to reset my rate limit
            if(req.status_code == 429):
                time.sleep(60)
            elif(req.status_code == 400):
                print("Out of images")
                with open("src/DataGathering/Logging/currentPage.txt", "w") as pageFile:
                    pageFile.write(str(i) + "\n")
                    pageFile.close
                return totalAccepted, ids
            else:
                #If I'm getting a non rate limit error code then I need to close to program so I dont spam the pixabay servers
                #with bad requests before I fix whatever issue I'm encountering. Logging the error text for posterity
                with open("src/DataGathering/Logging/badRequestsLog.txt", "a") as logFile:
                    logFile.write(str(req.status_code) + "\n")
                    logFile.write(req.text + "\n")
                    logFile.close()
                #with open("src/DataGathering/Logging/currentPage.txt", "w") as pageFile:
                #    pageFile.write(str(i) + "\n")
                #    pageFile.close
                file.close()
                sys.exit()

        jsonArray = req.json()['hits']

        #print("Length: " + str(len(jsonArray)))
        
        for item in jsonArray:
            retTags = item["tags"].split(", ")
            noBadTags = True
            for tag in retTags:
                #print("Current Tag: " + tag)
                if(tag.lower() in unacceptableWords):
                    noBadTags = False
                    break
            if(not noBadTags):
                continue

            containsEverySearch = True
            for x in range(0, len(tags)):
                if(not(tags[x] in retTags)):
                    containsEverySearch = False
                    break
            if(not containsEverySearch):
                continue
            
            if(not (item["id"] in ids)):
                totalAccepted += 1
                file.write("Id: " + str(item["id"]) + "\n")
                ids.append(item["id"])
                file.write("Tags: " + item["tags"] + "\n")
                file.write("URL: " + item["pageURL"] + "\n") 
                file.write("Small Picture URL: " + item["webformatURL"] + "\n")
                # print("Main URL: " + item["pageURL"])
                # print("Preview URL: " + item["previewURL"])
        time.sleep(60)
            
    return totalAccepted, ids

def main():
    if(sys.argv.__len__() < 2):
        print("Please Make Sure You Provide Your Pixaby API Key")
        sys.exit()
    key = sys.argv[1]

    # I hate having to save my current Page in its own file but I every different combintion of reading and writing i try to keep it all
    # in one file leeds to data loss so I'ma just do it this way
    #with open("src/DataGathering/Logging/currentPage.txt", "r") as file:
    #   currentPage = int(file.readline().strip())
    with open("src/DataGathering/bannedTags.txt", "r") as file:
        unacceptableWords = [line.strip() for line in file]
        file.close()

    currentPage = 0
    endPage = currentPage+1

    
    ids = []
    with open("src/DataGathering/Logging/acceptableAIImagesPixabay.txt", "r") as file:
        for line in file:
            ids.append(line[4:len(line)].strip())
            next(file, None)
            next(file, None)
        file.close()
    
    with open("src/DataGathering/Logging/acceptableAiImagesPixabay.txt", "a") as file:
        totalAcceptableImages = 0
        newImages, ids = requestImageURLS(10, file, ["ai generated ", "portrait", "man"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages
        newImages, ids = requestImageURLS(10,file, ["ai generated", "portrait", "woman"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages
        newImages, ids = requestImageURLS(10, file, ["ai generated ", "close up", "man"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages
        newImages, ids = requestImageURLS(10,file, ["ai generated", "close up", "woman"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages
        newImages, ids = requestImageURLS(10, file, ["ai generated ", "portrait"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages
        newImages, ids = requestImageURLS(10,file, ["ai generated", "close up"], unacceptableWords, currentPage, key, ids)
        totalAcceptableImages += newImages

        print(totalAcceptableImages)
        file.close()

    #with open("src/DataGathering/Logging/currentPage.txt", "w") as file:
    #    file.write(str(endPage) + "\n")
    #    file.close()
    

    

if(__name__ == '__main__'):
    main()
