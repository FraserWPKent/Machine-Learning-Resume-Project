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
    with open("src/DataGathering/bannedTags.txt") as file:
        badWordsArray = [line.strip() for line in file]

        for i in range(0, 10):
            # constructing the rest api access
            url = "https://pixabay.com/api/?key=" + key + "&q=Ai+Generated"
            for x in range(2, sys.argv.__len__()):
                url += "+" + sys.argv[x]
            url += "&image_type=photo&page="+str(i+1)+"&per_page=50&safesearch=true&category=people"
            print(url)
            req = requests.get(url=url)
            if (req.status_code != 200):
                print("Failed Request. Status Code: " + str(req.status_code))
                # If Im Overdoing it on the api requests wait for a minute to reset my limit
                if(req.status_code == 429):
                    time.sleep(70)

            jsonArray = req.json()['hits']
        
            count = 1
            for item in jsonArray:
                
                tags = item["tags"].split(", ")
                noBadTags = True
                for tag in tags:
                    if(not noBadTags):
                        continue
                    #print("Current Tag: " + tag)
                    if(tag.lower() in badWordsArray):
                        #print("Bad Tag: " + tag)
                        noBadTags = False
                if(noBadTags):
                    print(item["pageURL"])
                count += 1
            
            time.sleep(70)

        

    

if(__name__ == '__main__'):
    main()
