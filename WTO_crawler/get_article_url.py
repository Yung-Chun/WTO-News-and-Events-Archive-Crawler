from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import string
import random
import os.path
import pandas as pd

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'../geckodriver')

def get_code(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def get_elements_from_news(subMenu, page):
    df = []
    if int(page) >= 2006:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            title = tr.find_element(By.TAG_NAME, 'h3').text
            for li in tr.find_elements(By.TAG_NAME, 'li'):
                for link in li.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    elif 2003 <= int(page) and int(page) <= 2005:
        contentTable = driver.find_element(By.CLASS_NAME, 'contentTable')
        trs = contentTable.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            try:
                title = tr.find_element(By.CLASS_NAME, 'newsheadlinetext').text
                for body in tr.find_elements(By.CLASS_NAME, 'newsbodytext'):
                    for link in body.find_elements(By.TAG_NAME, 'a'):
                        type = link.text
                        url = link.get_attribute('href')
                        df.append([title, type, url])
            except:
                # title = row.find_element(By.CLASS_NAME, 'news1headlinetext').text
                title = tr.find_element(By.TAG_NAME, 'p').text
                for body in tr.find_elements(By.CLASS_NAME, 'news1bodytext'):
                    for link in body.find_elements(By.TAG_NAME, 'a'):
                        type = link.text
                        url = link.get_attribute('href')
                        df.append([title, type, url])

    elif 2000 <= int(page) and int(page) <= 2002:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for x in td.find_elements(By.CLASS_NAME, 'paracolourtext'):
                    if len(x.text) > 8:
                        title = x.text
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
    else:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                title = None
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    df = pd.DataFrame(df, columns=['title', 'type', 'url'])

    return df

def get_elements_from_press(subMenu, page):
    df = []
    if int(page) >= 2018:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        rows = centerCol.find_elements(By.CLASS_NAME, 'row')
        for row in rows:
            title = row.find_element(By.TAG_NAME, 'h3').text
            for li in row.find_elements(By.TAG_NAME, 'li'):
                for link in li.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    elif 2006 <= int(page) and int(page) <= 2017:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for x in td.find_elements(By.TAG_NAME, 'h3'):
                    title = x.text
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
    
    else:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    title = link.text
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    df = pd.DataFrame(df, columns=['title', 'type', 'url'])

    return df

def get_elements_from_dg(subMenu, page):
    df = []
    if idx >= 3:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    title = link.text
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    elif idx == 2:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for x in td.find_elements(By.TAG_NAME, 'h3'):
                    if len(x.text) > 8:
                        title = x.text
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
        
    else:
        newsArc = driver.find_element(By.ID, 'newsArc')
        rows = newsArc.find_elements(By.CLASS_NAME, 'row')
        for row in rows:
            title = row.find_element(By.TAG_NAME, 'h3').text
            for li in row.find_elements(By.TAG_NAME, 'li'):
                for link in li.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
        
    df = pd.DataFrame(df, columns=['title', 'type', 'url'])
    
    return df

def get_elements_from_subject(subMenu, page):
    df = []
    if idx <= 25 or (27 <= idx and idx <= 37) or (39 <= idx and idx <= 114) or idx >= 116:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        rows = centerCol.find_elements(By.CLASS_NAME, 'row')
        
        for row in rows:
            title = row.find_element(By.TAG_NAME, 'h3').text
            for li in row.find_elements(By.TAG_NAME, 'li'):
                for link in li.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
    
    elif idx in [26, 38]:
        newsArc = driver.find_element(By.ID, 'newsArc')
        rows = newsArc.find_elements(By.CLASS_NAME, 'row')
        for row in rows:
            title = row.find_element(By.TAG_NAME, 'h3').text
            for li in row.find_elements(By.TAG_NAME, 'li'):
                for link in li.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])
    
    elif idx == 115:
        pass

    else:
        centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
        trs = centerCol.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                for x in td.find_elements(By.TAG_NAME, 'h3'):
                    if len(x.text) > 8:
                        title = x.text
                for link in td.find_elements(By.TAG_NAME, 'a'):
                    type = link.text
                    url = link.get_attribute('href')
                    df.append([title, type, url])

    df = pd.DataFrame(df, columns=['title', 'type', 'url'])

    return df

# set path to store the data
if not os.path.exists(f'../WTO_data_article/'):
    os.mkdir(f'../WTO_data_article/')

# read json file
with open('targetMenuUrlDict.json', 'r') as fp:
    targetMenuUrlDict = json.load(fp)
   
    
for subMenu in targetMenuUrlDict.keys():
    # mission today
    if subMenu in [
        'News archives', 
        'Press releases', 
    #    'DG speeches', 
       'Subject archives'
                       ]:
        pass

    else:
        print(subMenu)
        
        # set path to store the data
        menuPathName = subMenu.replace(' ', '_').replace(',', '_')
        if not os.path.exists(f'../WTO_data_article/{menuPathName}'):
            os.mkdir(f'../WTO_data_article/{menuPathName}')
        path = os.path.abspath(f'../WTO_data_article/{menuPathName}')

        # go to the page of each submenu
        for idx, page in enumerate(targetMenuUrlDict[subMenu].keys()):
            if idx >= 3:
                print(page)
                pagePageName = page.replace(' ', '_')
                url = targetMenuUrlDict[subMenu][page]
                driver.get(url)
                print(idx, subMenu, page, url)
                time.sleep(10) 
                
                if subMenu == 'News archives':
                    df = get_elements_from_news(subMenu, page)

                elif subMenu == 'Press releases':
                    df = get_elements_from_press(subMenu, page)

                elif subMenu == 'DG speeches':
                    df = get_elements_from_dg(subMenu, page)

                else:
                    df = get_elements_from_subject(subMenu, page)

                # print langth of each column
                print(f'num of title: {len(set(df.title))}')
                print(f'num of type: {len(set(df.type))}')
                print(f'num of url: {len(set(df.url))}')

                # export articleDict to csv file
                with open(os.path.join(path, f'{menuPathName}_{pagePageName}.csv'), 'w') as fp:
                    df.to_csv(fp, index=False)
                    
                time.sleep(5)   

driver.close()
            