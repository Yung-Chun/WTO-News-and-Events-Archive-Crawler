from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import pandas as pd
import time
from datetime import datetime
import os.path
from pathlib import Path
import re
import random

options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path=r'../geckodriver', options=options)

 # title_extraction_methods
def title_extraction_1(introTextDiv):
    title = introTextDiv.find_element(By.TAG_NAME, 'h1').text
    return title

def title_extraction_2(introTextDiv):
    title = introTextDiv.find_element(By.CLASS_NAME, 'pagetitletext').text
    return title

def title_extraction_3(introTextDiv):
    title = introTextDiv.find_element(By.CLASS_NAME, 'maintitletext').text
    return title

title_extraction_methods = [title_extraction_1, title_extraction_2, title_extraction_3]

def label_extraction_1(introTextDiv):
    label = ' '.join([kt.text for kt in introTextDiv.find_elements(By.CLASS_NAME, 'kickertext')])
    return label

def label_extraction_2(introTextDiv):
    label = introTextDiv.find_element(By.TAG_NAME, 'p').text
    return label

label_extraction_methods = [label_extraction_1, label_extraction_2]
                        
# date_extraction_methods
months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 
          'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

def date_extraction_1(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = introTextDiv.find_element(By.CLASS_NAME, 'paralargecolourtext').text
    return date

def date_extraction_2(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = ' '.join([kt.text for kt in introTextDiv.find_elements(By.CLASS_NAME, 'kickertext')])
    return date

def date_extraction_3(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = ' '.join([pt.text for pt in introTextDiv.find_elements(By.CLASS_NAME, 'paranormaltext')])
    return date

def date_extraction_4(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = introTextDiv.find_element(By.TAG_NAME, 'p').text
    return date

def date_extraction_5(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = ' '.join([br.text for br in introTextDiv.find_elements(By.TAG_NAME, 'br')])
    return date

def date_extraction_6(driver):
    introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
    date = ' '.join(introTextDiv.text.split('\n')[:4])
    return date

def date_extraction_7(driver):
    centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
    date = centerCol.find_element(By.CLASS_NAME, 'parasmalltext').text
    return date

def date_extraction_8(driver):
    centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
    date = centerCol.find_element(By.TAG_NAME, 'b').text
    return date

def date_extraction_9(driver):
    centerCol = driver.find_element(By.CLASS_NAME, 'centerCol')
    date = centerCol.find_element(By.TAG_NAME, 'p').text
    return date

def date_extraction_10(driver):
    rightCol = driver.find_element(By.CLASS_NAME, 'rightCol')
    date = datetime.strptime(rightCol.text.split('\n')[3], "%d.%m.%Y").strftime("%d %B %Y")
    return date

date_extraction_methods = [date_extraction_1, date_extraction_2, date_extraction_3, date_extraction_4, 
                           date_extraction_5, date_extraction_6, date_extraction_7, date_extraction_8,
                           date_extraction_9, date_extraction_10]

# outboundLinks extraction
def extract_linkdoldoc(outboundLink):
    if 'javascript' in outboundLink:
        linkdoldoc = re.search(r"'(.*?)'", outboundLink)[1]
        outboundLink = f'https://docs.wto.org/dol2fe/Pages/SS/directdoc.aspx?filename=q:{linkdoldoc}&Open=True'
    return outboundLink

# read each json file from WTO_data_article/News_archives
path = os.path.abspath('../WTO_data_article')

all_urls = set()
for folder in os.listdir(path):
    print(folder)
    sub_urls = set()
    if not '.' in folder:
        for file in os.listdir(path + '/' + folder):
            # print(file)
            data = pd.read_csv(path + '/' + folder + '/' + file)
            sub_urls = sub_urls.union(set(data['url']))
            all_urls = all_urls.union(set(data['url']))
            sub_urls = {x for x in sub_urls if x == x}
        print('category unique:', len(sub_urls))
all_urls = {x for x in all_urls if x == x}
print('total unique:', len(all_urls), end='\n\n')

# if there is no all_article_content.json, create one, else read it
if not os.path.exists(f'../WTO_data_article/all_article_content.json'):
    with open(path + '/all_article_content.json', 'w') as fp:
        json.dump({}, fp)
        all_article_content = {}
else:
    with open(path + '/all_article_content.json', 'r') as fp:
        all_article_content = json.load(fp)
        print(f'there are already {len(all_article_content)} articles in the json file')
        print(f'{len(all_urls) - len(all_article_content)} articles to go', end='\n\n')

# if there is no fail_record.json, create one, else read it
if not os.path.exists(f'../WTO_data_article/fail_record.json'):
    with open(path + '/fail_record.json', 'w') as fp:
        json.dump({}, fp)
        fail_record = {}
else:
    with open(path + '/fail_record.json', 'r') as fp:
        fail_record = json.load(fp)

idx = len(all_article_content)
for url in all_urls:
    if url in all_article_content.keys() or 'htm' not in url:
        continue

    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f'mission {idx}: going to {url}')
        idx += 1

        if 'blogs_e' in url:
            try:
                driver.get(url)
                title = driver.find_element(By.ID, 'blogtitle').text
                date = driver.find_element(By.ID, 'blogpostdate').text

                try:
                    content = driver.find_element(By.ID, 'blogtext').text
                except:
                    content = driver.find_element(By.CLASS_NAME, 'blogtext').text

                try:
                    outboundLinks = [a.get_attribute('href') for a in driver.find_element(By.ID, 'blogtext').find_elements(By.TAG_NAME, 'a')]
                    outboundLinks = [extract_linkdoldoc(outboundLink) for outboundLink in outboundLinks]
                    outboundLinksText = [a.text for a in driver.find_element(By.ID, 'blogtext').find_elements(By.TAG_NAME, 'a')]
                except:
                    outboundLinks = []
                    outboundLinksText = []

                # Update the articleDict
                articleDict = {url: {'title': title, 
                                    'raw_date': date, 
                                    'raw_label': None, 
                                    'abstract': None, 
                                    'content': content, 
                                    'outboundLinks': outboundLinks, 
                                    'outboundLinksText': outboundLinksText}}
                all_article_content.update(articleDict)

                # add articleDict to json file
                print('sussessfully get content for:', title)
                print('-----------------------')
                with open(f'../WTO_data_article/all_article_content.json', 'w') as fp:
                    json.dump(all_article_content, fp)

            except Exception as e:
                print('fail to get content for:', url)
                print(e)
                print('-----------------------')
                fail_record.update({url:str(e)})
                with open(f'../WTO_data_article/fail_record.json', 'w') as fp:
                    json.dump(fail_record, fp)
                continue
            
        else:
            try:
                driver.get(url)
                introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
                
                # content
                content = driver.find_element(By.CLASS_NAME, 'centerCol').text

                # title
                for title_extraction_method in title_extraction_methods:
                    try:
                        title = title_extraction_method(introTextDiv)
                        break
                    except:
                        pass

                # abstract
                try:
                    abstract = introTextDiv.find_element(By.CLASS_NAME, 'paralargetext').text
                except:
                    abstract = None

                # label
                for label_extraction_method in label_extraction_methods:
                    try:
                        label = title_extraction_method(introTextDiv)
                        if len(label) > 0:
                            break
                    except:
                        label = None
                
                # date
                for date_extraction_method in date_extraction_methods:
                    try:
                        temp_date = date_extraction_method(driver)
                        for m in months:
                            if m in temp_date.upper():
                                date = temp_date
                                break
                    except:
                        pass
                    
                # outboundLinks
                try:
                    outboundLinks = [a.get_attribute('href') for a in driver.find_element(By.CLASS_NAME, 'centerCol').find_elements(By.TAG_NAME, 'a')]
                    outboundLinks = [extract_linkdoldoc(outboundLink) for outboundLink in outboundLinks]
                    outboundLinksText = [a.text for a in driver.find_element(By.CLASS_NAME, 'centerCol').find_elements(By.TAG_NAME, 'a')]
                except:
                    outboundLinks = []
                    outboundLinksText = []

                # Update the articleDict
                articleDict = {url: {'title': title, 
                                    'raw_date': date, 
                                    'raw_label': label, 
                                    'abstract': abstract, 
                                    'content': content, 
                                    'outboundLinks': outboundLinks, 
                                    'outboundLinksText': outboundLinksText}}
                all_article_content.update(articleDict)

                # add articleDict to json file
                print('sussessfully get content for:', title)
                print('-----------------------')
                with open(f'../WTO_data_article/all_article_content.json', 'w') as fp:
                    json.dump(all_article_content, fp)

            except Exception as e:
                print('fail to get content for:', url)
                print(e)
                print('-----------------------')
                fail_record.update({url:str(e)})
                with open(f'../WTO_data_article/fail_record.json', 'w') as fp:
                    json.dump(fail_record, fp)
                continue

    # time.sleep(random.randint(0, 5)) 

driver.close()



            