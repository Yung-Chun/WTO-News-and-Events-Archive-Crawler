from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import json
import pandas as pd
import time
import os.path
from pathlib import Path
import re
import random

options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path=r'../geckodriver', options=options)

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
print('total unique:', len(all_urls))

# if there is no all_article_content.json, create one, else read it
if not os.path.exists(f'../WTO_data_article/all_article_content.json'):
    with open(path + '/all_article_content.json', 'w') as fp:
        json.dump({}, fp)
        all_article_content = {}
else:
    with open(path + '/all_article_content.json', 'r') as fp:
        all_article_content = json.load(fp)
        print(f'there are already {len(all_article_content)} articles in the json file')
        print(f'{len(all_urls) - len(all_article_content)} articles to go')

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
        
        try:
            driver.get(url)
            introTextDiv = driver.find_element(By.CLASS_NAME, 'introTextDiv')
            
            # Extract data once the WebElement is stale
            for kickertext in introTextDiv.find_elements(By.CLASS_NAME, 'kickertext'):
                if kickertext.find_element(By.TAG_NAME, 'b'):
                    label = kickertext.find_element(By.TAG_NAME, 'b').text
                else:
                    date = kickertext.text
            abstract = introTextDiv.find_element(By.CLASS_NAME, 'paralargetext').text
            title = introTextDiv.find_element(By.TAG_NAME, 'h1').text
            content = driver.find_element(By.CLASS_NAME, 'centerCol').text

            try:
                outboundLinks = [a.get_attribute('href') for a in driver.find_element(By.CLASS_NAME, 'centerCol').find_elements(By.TAG_NAME, 'a')]
                outboundLinks = [extract_linkdoldoc(outboundLink) for outboundLink in outboundLinks]
                outboundLinksText = [a.text for a in driver.find_element(By.CLASS_NAME, 'centerCol').find_elements(By.TAG_NAME, 'a')]
            except:
                outboundLinks = []
                outboundLinksText = []

            # Update the articleDict
            articleDict = {url: {'date': date, 
                                'label': label, 
                                'abstract': abstract, 
                                'title': title, 
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

    time.sleep(random.randint(0, 5)) 

driver.close()



            