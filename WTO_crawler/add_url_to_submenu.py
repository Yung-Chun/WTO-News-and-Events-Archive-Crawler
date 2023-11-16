from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# read json file
with open('targetMenuDict.json', 'r') as fp:
    targetMenuDict = json.load(fp)

targetSubMenuLst = []
for value in targetMenuDict.values():
    targetSubMenuLst += value

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'/Users/ycchen/geckodriver')
driver.get("https://www.wto.org/english/news_e/news_e.htm#archives")

# get all urls under TreeviewSpanArea and store needed in a dictionary
subMenuUrlLst = driver.find_elements(By.TAG_NAME, 'a')

subMenuUrlDict = {}
for subMenuUrl in subMenuUrlLst:
    href = subMenuUrl.get_attribute('href')
    text = subMenuUrl.get_attribute('text')
    try:
        if text in targetSubMenuLst:
            print(text, href)
            subMenuUrlDict[text] = href
    except:
        pass

targetMenuUrlDict = {}

for key in targetMenuDict.keys():
    targetMenuUrlDict[key] = {}

    for subMenu in targetMenuDict[key]:

        if key == 'News archives':
            subString = 'news' + str(subMenu[2:]) + '_e'
            url = f'https://www.wto.org/english/news_e/{subString}/{subString}.htm'
    
        elif key == 'Press releases':
            subString = 'pres' + str(subMenu[2:]) + '_e'
            url = f'https://www.wto.org/english/news_e/{subString}/{subString}.htm'
            
        else:
            try:
                url = subMenuUrlDict[subMenu]
            except Exception as e:
                print(e)
                print(f'no url for {subMenu}')
                pass

        # add value to targetMenuUrlDict
        targetMenuUrlDict[key][subMenu] = url

# export targetMenuDict to json file
with open('targetMenuUrlDict.json', 'w') as fp:
    json.dump(targetMenuUrlDict, fp)

driver.close()