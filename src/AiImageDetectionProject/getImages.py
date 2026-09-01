import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
from seleniumbase import Drivers
import time
import random
def main():
    print("Starting:")
    

    options = Options()

    #options.add_argument("-headless")
    #options.add_argument("-private")
    options.add_argument("-profile=C:/Users/fwpke/AppData/Roaming/Mozilla/Firefox/Profiles/7DqtqHHk.Profile 1")

    driver = webdriver.Firefox(options=options)

    driver.get("https://google.com/")

    #randGenerator = random.Random()
    #currentTime = int(time.time())
    #randGenerator.seed(currentTime)
    #waitTime = randGenerator.random()*5
    #print(currentTime)
    #print(waitTime)
    time.sleep(10)  
    #print("Ending")
    #driver.implicitly_wait(30)
      
    title = driver.title
    print(title)

    driver.quit()

if(__name__ == '__main__'):
    main()
