from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import string
import random

def get_code(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

# read json file
with open('targetMenuDict.json', 'r') as fp:
    targetMenuDict = json.load(fp)

targetMenuLst = ['News archives', 'Press releases', 'DG speeches', 'Subject archives']

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'/Users/ycchen/geckodriver')

for subMenu in targetMenuDict['News archives']:
    # create a new json file for each submenu
    with open(f'../WTO_data/{subMenu}.json', 'w') as fp:
        json.dump({}, fp)

    # go to the page of each submenu
    print(subMenu)
    subString = 'news' + str(subMenu[2:]) + '_e'
    url = f'https://www.wto.org/english/news_e/{subString}/{subString}.htm'
    print(url)
    driver.get(url)
    time.sleep(3)
    

    # get url of all news
    elems = driver.find_elements(By.CLASS_NAME, 'paracolourtext')
    newsTypeLst = [elem.text for elem in elems]
    newsUrlLst = [elem.get_attribute("href") for elem in elems]
    print(f'length of newsTypeLst: {len(newsTypeLst)}')
    print(f'length of newsUrlLst: {len(newsUrlLst)}')
    if len(newsTypeLst) != len(newsUrlLst):
        print('length of newsTypeLst and newsUrlLst are not equal')
        break
    time.sleep(3)

    for idx in range(len(newsUrlLst)):
        article_id = get_code(32)
        article_url = newsUrlLst[idx]
        article_type = newsTypeLst[idx]

        driver.get(article_url)
        print(f'go to {article_url}')
        time.sleep(3)
        driver.refresh()

        try:
            introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
            # Create a WebDriverWait instance with a timeout
            wait = WebDriverWait(driver, 10, 1)  # Adjust the timeout as needed
            # Wait until the WebElement becomes stale
            wait.until(EC.staleness_of(introTextDiv))
            
            date = introTextDiv.find_elements(By.TAG_NAME, 'p')[0].text
            label = introTextDiv.find_elements(By.TAG_NAME, 'p')[1].text
            abstract = introTextDiv.find_elements(By.TAG_NAME, 'p')[2].text
            title = introTextDiv.find_element(By.TAG_NAME, 'h1').text
            content = driver.find_element(By.CLASS_NAME, 'centerCol').text

            data = {
                'menu': 'News archives',
                subMenu: {
                    article_id: {
                        'article_url': article_url,
                        'article_type': article_type,
                        'title': title,
                        'date': date,
                        'label': label,
                        'abstract': abstract,
                        'content': content
                    }
                }
            }
        
        except Exception as e:
            print(e)
            print(article_url)
            print(article_type)
            print(article_id)
            print('-----------------------')
            continue
        
        # update to json file
        with open(f'../WTO_data/{subMenu}.json', 'a') as fp:
            json.dump(data, fp)

        break

        time.sleep(1)
    time.sleep(4)

driver.close()