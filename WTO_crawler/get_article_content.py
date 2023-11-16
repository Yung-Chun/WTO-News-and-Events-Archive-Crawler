from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import os.path
from pathlib import Path

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'./geckodriver')

def check_articleIdLst(file, articleIdLst):
    if len(articleIdLst) != len(set(articleIdLst)):
        print(f'{file.name} has duplicate articleId')
        return False
    
    elif len(articleIdLst) == 0:
        print(f'{file.name} is empty')
        return False
    
    else:
        print(f'{file.name} is valid')
        return True

targetMenuLst = ['News archives', 'Press releases'] #, 'DG speeches', 'Subject archives'

# read each json file from WTO_data_article/News_archives
path = Path(fr'../WTO_data_article/News_archives')

for year in range(2023, 1997, -1):
    # read json file
    with open(f'../WTO_data_article/News_archives/News_archives_{year}.json', 'r') as fp:
            articleDict = json.load(fp)
            articleIdLst = articleDict.keys()
            
    if check_articleIdLst(fp, articleIdLst):
        for idx in articleIdLst:
            print(f'go to {articleDict[idx]["url"]}')
            driver.get(articleDict[idx]['url'])
            time.sleep(3)

            try:
                introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
                # Create a WebDriverWait instance with a timeout
                # wait = WebDriverWait(driver, 20, 1)  # Adjust the timeout as needed
                # Wait until the WebElement becomes stale
                # wait.until(EC.staleness_of(introTextDiv))
                
                # Extract data once the WebElement is stale
                date, label, abstract = [p.text for p in introTextDiv.find_elements(By.TAG_NAME, 'p')[:3]]
                title = introTextDiv.find_element(By.TAG_NAME, 'h1').text
                content = driver.find_element(By.CLASS_NAME, 'centerCol').text

                # Update the articleDict
                articleDict[idx]['date'] = date
                articleDict[idx]['label'] = label
                articleDict[idx]['abstract'] = abstract
                articleDict[idx]['title'] = title
                articleDict[idx]['content'] = content

                # save the articleDict to json file
                with open(f'../WTO_data_article/{fp.name}', 'w') as fp:
                    json.dump(articleDict, fp)
                time.sleep(2)

            except Exception as e:
                print(e)
                print(idx)
                print(articleDict[idx]['url'])
                print('-----------------------')
                continue

    fp.close()
    time.sleep(5) 

driver.close()



            