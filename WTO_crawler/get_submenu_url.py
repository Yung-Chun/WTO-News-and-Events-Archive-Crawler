from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
from tqdm import tqdm

targetMenuLst = ['News archives', 'Press releases', 'DG speeches', 'Subject archives']

# open the browser and get the page
options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path=r'../geckodriver', options=options)

print('Going to the WTO website...')
main_url = 'https://www.wto.org/english/news_e/news_e.htm#'
driver.get(main_url)

# get all subjects and urls under TreeviewSpanArea
TreeviewSpanArea = driver.find_elements(By.CLASS_NAME, 'TreeviewSpanArea')[1]
subMenu = TreeviewSpanArea.find_elements(By.TAG_NAME, 'a')

subMenuText = [subMenuText.get_attribute('text') for subMenuText in subMenu]
subMenuUrl = [subMenuUrl.get_attribute('href') for subMenuUrl in subMenu]

# store in a dictionary
targetMenuUrlDict = {}
targetMenu_idx = 0
idx = 0

for url in tqdm(subMenuUrl, desc='Storing subMenuUrl'):
    if url == main_url:
        targetMenu = targetMenuLst[targetMenu_idx]
        targetMenuUrlDict.update({targetMenu:{}})
        targetMenu_idx += 1
        idx += 1
        continue
    
    targetMenuUrlDict[targetMenu].update({subMenuText[idx]: subMenuUrl[idx]})
    idx += 1

# export targetMenuDict to json file
with open('targetMenuUrlDict.json', 'w') as fp:
    json.dump(targetMenuUrlDict, fp)

driver.close()

