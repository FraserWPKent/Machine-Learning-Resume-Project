import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
import os
import sys
import time
import random

import requests

def testngSelenium():
    options = Options()
    
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

def main():

    if(sys.argv.__len__() < 2):
        print("Please Make Sure You Provide Your Pixaby API Key")
        sys.exit()

    key = sys.argv[1]

    # I hate having to save my current Page in its own file but I every different combintion of reading and writing i try to keep it all
    # in one file leeds to data loss so I'ma just do it this way
    with open("src/DataGathering/currentPage.txt", "r") as file:
       currentPage = int(file.readline().strip())
    with open("src/DataGathering/bannedTags.txt", "r") as file:
        unacceptableWords = [line.strip() for line in file]
        file.close()

    endPage = currentPage+1
    
    with open("src/DataGathering/acceptableImages.txt", "a") as file:
        totalAcceptableImages = 0
        for i in range(currentPage, endPage):
            # constructing the rest api access
            url = "https://pixabay.com/api/?key=" + key + "&q=Ai+Generated"
            for x in range(2, sys.argv.__len__()):
                url += "+" + sys.argv[x]
            url += "&image_type=photo&page="+str(i+1)+"&per_page=50&safesearch=true&category=people"
            #print(url)
            req = requests.get(url=url)
            if (req.status_code != 200):
                print("Failed Request. Status Code: " + str(req.status_code))
                # If Im Overdoing it on the api requests wait for a bit to reset my rate limit
                if(req.status_code == 429):
                    time.sleep(120)
                else:
                    #If I'm getting a non rate limit error code then I need to close to program so I dont spam the pixabay servers
                    #with bad requests before I fix whatever issue I'm encountering. Logging the error text for posterity
                    with open("src/DataGathering/badRequestsLog.txt", "a") as logFile:
                        logFile.write(str(req.status_code) + "\n")
                        logFile.write(req.text + "\n")
                        logFile.close()
                    sys.exit()

            jsonArray = req.json()['hits']

            #count = 1
            for item in jsonArray:
                tags = item["tags"].split(", ")
                noBadTags = True
                for tag in tags:
                    if(not noBadTags):
                        continue
                    #print("Current Tag: " + tag)
                    if(tag.lower() in unacceptableWords):
                        #print("Bad Tag: " + tag)
                        noBadTags = False
                if(noBadTags):
                    totalAcceptableImages += 1
                    #print(item["pageURL"])
                    file.write("Tags: " + item["tags"] + "\n")
                    #print(type(item["tags"]))
                    file.write("URL: " + item["pageURL"] + "\n")
                #count += 1
            time.sleep(60)
        file.close()

    with open("src/DataGathering/currentPage.txt", "w") as file:
        file.write(str(endPage) + "\n")
    

    

if(__name__ == '__main__'):
    main()
