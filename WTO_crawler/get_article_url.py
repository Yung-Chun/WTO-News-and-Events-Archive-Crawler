from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
import time
import string
import random
import os.path

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'./geckodriver')

def get_code(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def get_elements_from_news(subMenu):
    
    if int(page) <= 2002:
        elems = driver.find_element(By.CLASS_NAME, 'centerCol').find_elements(By.TAG_NAME, 'a') 
        urlLst = [elem.get_attribute('href') for elem in elems]
        typeLst = [elem.text for elem in elems]
        titleLst = [titleElem.text for titleElem in driver.find_elements(By.TAG_NAME, 'h3') ]

    elif 2003 <= int(page) and int(page) <= 2005:
        urlLst, typeLst = [], []
        class_names = ['news1bodytext', 'newsbodytext']
        for class_name in class_names:
            elems = driver.find_elements(By.CLASS_NAME, class_name)
            titleLst = [titleElem.text for titleElem in driver.find_elements(By.TAG_NAME, 'h3') ]
            for elem in elems:
                try:
                    urlLst.append(elem.find_element(By.TAG_NAME, 'a').get_attribute('href'))
                    typeLst.append(elem.find_element(By.TAG_NAME, 'a').text)
                except:
                    pass

    else:
        elems = driver.find_elements(By.CLASS_NAME, 'paracolourtext') #since2006
        urlLst = [elem.get_attribute("href") for elem in elems]
        typeLst = [elem.text for elem in elems]
        titleLst = [titleElem.text for titleElem in driver.find_elements(By.TAG_NAME, 'h3') ]

    articleIdLst = [get_code(32) for i in range(len(urlLst))]

    return titleLst, typeLst, urlLst, articleIdLst

def get_elements_from_press(subMenu):
    if int(page) <= 2005:
        elems = driver.find_element(By.CLASS_NAME, 'contentTable').find_elements(By.TAG_NAME, 'a') 

    else:
        elems = driver.find_elements(By.CLASS_NAME, 'paracolourtext') #since2006

    urlLst = [elem.get_attribute("href") for elem in elems]
    typeLst = [elem.text for elem in elems]
    articleIdLst = [get_code(32) for i in range(len(urlLst))]
    titleLst = [titleElem.text for titleElem in driver.find_elements(By.TAG_NAME, 'h3') ]

    return titleLst, typeLst, urlLst, articleIdLst

def get_elements_from_dg(subMenu):
    if idx >= 3:
        elems = driver.find_element(By.CLASS_NAME, 'contentTable').find_elements(By.TAG_NAME, 'a') 
        
    else:
        elems = driver.find_elements(By.CLASS_NAME, 'paracolourtext')
    
    
    urlLst = [elem.get_attribute("href") for elem in elems]
    typeLst = [elem.text for elem in elems]
    articleIdLst = [get_code(32) for i in range(len(urlLst))]

    return typeLst, urlLst, articleIdLst

def get_elements_from_subject(subMenu):
    elems = driver.find_elements(By.CLASS_NAME, 'paracolourtext')
    
    urlLst = [elem.get_attribute("href") for elem in elems]
    typeLst = [elem.text for elem in elems]
    articleIdLst = [get_code(32) for i in range(len(urlLst))]

    return typeLst, urlLst, articleIdLst

# set path to store the data
if not os.path.exists(f'../WTO_data_article/'):
    os.mkdir(f'../WTO_data_article/')

# read json file
with open('targetMenuUrlDict.json', 'r') as fp:
    targetMenuUrlDict = json.load(fp)
   
    
for subMenu in targetMenuUrlDict.keys():
    # mission today
    if subMenu in [
        # 'News archives', 
        # 'Press releases', 
       'DG speeches', 
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
            if idx >= 0:
                print(page)
                pagePageName = page.replace(' ', '_')
                url = targetMenuUrlDict[subMenu][page]
                driver.get(url)
                print(idx, subMenu, page, url)
                time.sleep(10) 
                
                if subMenu == 'News archives':
                    titleLst, typeLst, urlLst, articleIdLst = get_elements_from_news(subMenu)

                elif subMenu == 'Press releases':
                    titleLst, typeLst, urlLst, articleIdLst = get_elements_from_press(subMenu)

                elif subMenu == 'DG speeches':
                    titleLst, typeLst, urlLst, articleIdLst = get_elements_from_dg(subMenu)

                else:
                    titleLst, typeLst, urlLst, articleIdLst = get_elements_from_subject(subMenu)

                # print langth of each list
                print(f'length of typeLst: {len(typeLst)}')
                print(f'length of urlLst: {len(urlLst)}')
                print(f'length of articleIdLst: {len(articleIdLst)}')

                # convert list to dictionary
                articleDict = {}
                for idx in range(len(urlLst)):
                    articleDict[articleIdLst[idx]] = {'menu': subMenu,
                                                      'title': titleLst[idx],
                                                      'type': typeLst[idx], 
                                                      'url': urlLst[idx]}
                    
                # export articleDict to json file
                with open(os.path.join(path, f'{menuPathName}_{pagePageName}.json'), 'w') as fp:
                    json.dump(articleDict, fp)

                time.sleep(5)   

driver.close()
            