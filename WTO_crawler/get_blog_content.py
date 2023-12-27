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

blog_urls = set()
for folder in os.listdir(path):
    print(folder)

    if not '.' in folder:
        for file in os.listdir(path + '/' + folder):
            # print(file)
            data = pd.read_csv(path + '/' + folder + '/' + file)
            for url in data['url']:
                if 'blogs_e' in str(url):
                    blog_urls.add(url)
          
print('total unique (blog):', len(blog_urls))

# if there is no all_article_content.json, create one, else read it
if not os.path.exists(f'../WTO_data_article/all_article_content.json'):
    with open(path + '/all_article_content.json', 'w') as fp:
        json.dump({}, fp)
        all_article_content = {}
else:
    with open(path + '/all_article_content.json', 'r') as fp:
        all_article_content = json.load(fp)
        crawled_blogs = set(all_article_content.keys()).intersection(blog_urls)
        print(f'there are already {len(crawled_blogs)} blogs in the json file')
        print(f'{len(blog_urls) - len(crawled_blogs)} blogs to go')

# if there is no fail_record.json, create one, else read it
if not os.path.exists(f'../WTO_data_article/fail_record.json'):
    with open(path + '/fail_record.json', 'w') as fp:
        json.dump({}, fp)
        fail_record = {}
else:
    with open(path + '/fail_record.json', 'r') as fp:
        fail_record = json.load(fp)

idx = len(crawled_blogs)

for url in blog_urls:
    if url in all_article_content.keys() or 'htm' not in url:
        continue
    
    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f'mission {idx}: going to {url}')
        idx += 1
        
        try:
            driver.get(url)
            title = driver.find_element(By.ID, 'blogtitle').text
            abstract = None
            label = None
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



            