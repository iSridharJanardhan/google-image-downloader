import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import os
import math

#define constants 
chrome_driver = "your path to chrome driver"

#input query
query = input("Image needed to download:")
download_number = input("Number of images to download")

url = "https://www.google.com/search?q=" + query + "&tbm=isch"
dirs = query.replace(" ", "-")

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
# options.add_argument('--headless')

browser = webdriver.Chrome(chrome_driver, options=options)
browser.get(url)

element = browser.find_element_by_tag_name('body')

if not os.path.exists(dirs):
    os.mkdir(dirs)
iterate_range = math.floor(int(download_number) / 20)
for i in range(iterate_range):
    element.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)

page_source = browser.page_source

soup = BeautifulSoup(page_source, 'lxml')
images = soup.find_all('img')
urls = []
for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

count = 0
if urls:
    for url in urls:
        try:
            res = requests.get(url, verify=False, stream=True)
            rawdata = res.raw.read()
            with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                f.write(rawdata)
                count += 1
        except Exception as e:
            print('Failed to write rawdata.')
            print(e)