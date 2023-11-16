from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# open the browser and get the page
driver = webdriver.Firefox(executable_path=r'/Users/ycchen/geckodriver')
driver.get("https://www.wto.org/english/news_e/news_e.htm#archives")

# get all titles under TreeviewSpanArea and store needed in a dictionary
subMenuLst = driver.find_elements(By.CLASS_NAME, 'TreeviewSpanArea') #可以取出list所有標題
targetMenuDict = {}
targetMenuLst = ['News archives', 'Press releases', 'DG speeches', 'Subject archives']
for subMenu in subMenuLst[1].text.split('\n'):
    if subMenu in targetMenuLst:
        key = subMenu
        targetMenuDict[key] = []
    else:
        targetMenuDict[key].append(subMenu)

# export targetMenuDict to json file
with open('targetMenuDict.json', 'w') as fp:
    json.dump(targetMenuDict, fp)

driver.close()


# for elem in elems:
#     if elem.text == '2022':
#         print(elem.text)
#         print(elem)
#         elem.click()
# print([elem.text for elem in elems])

# elem = driver.find_element(By.PARTIAL_LINK_TEXT, '2021— Ngozi Okonjo-Iweala')
# print(elem.text)
# print(elem)
# elem.click()


