from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os
from tqdm import tqdm


def ohLinkFinder(category_id: str, howMany: int):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)

    # url = f"https://ohou.se/cards/feed?query={toSearch}"
    url = f"https://ohou.se/store/category?category=0&order=popular"
    driver.get(url)

    
    
    index_list = driver.find_elements(By.XPATH, '//*[@class="commerce-category-tree__entry"]/*[@class="commerce-category-tree__entry__header"]/*[@class="commerce-category-tree__entry__title"]')
    index_count = 0
    inner_page_list = []

    for div in index_list:
        div.click()
        print(div.get_attribute('innerText'))
        if div.get_attribute('innerText') != '야외가구':
            continue
        inner_index_list = div.parent.find_elements(By.XPATH, '//*[@class="open expanded"]/*[@class="commerce-category-tree commerce-category-tree__entry__children"]/*[@class="commerce-category-tree__entry"]/*[@class="commerce-category-tree__entry__header"]/*[@class="commerce-category-tree__entry__title"]')
        inner_list = []

        for inner_div in inner_index_list:
            inner_list.append({'page_url':inner_div.get_attribute('href'),'page_name':inner_div.get_attribute('innerText')})

        inner_page_list.append(inner_list)
    for inner_list in inner_page_list:
        for inner_page in inner_list:
            os.makedirs(inner_page['page_name'],exist_ok=True)
            driver.get(inner_page['page_url'])
            time.sleep(5)
            # os.makedirs(inner_page['page_name'],exist_ok=True)
            linkSet = set()
            last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            while len(linkSet)<= howMany:
                linkList = driver.find_elements(By.XPATH, '//*[@class="production-item-image production-item__image"]/*[@class="image"]')
                def get_link():
                    for div in linkList:
                        
                        link = div.get_attribute('src')
                        if link is None:
                            continue
                        link = link.replace('w=360&h=360&c=c&q=0.8', 'w=1700&h=1700')
                        linkSet.add(link)
                try:
                    get_link()
                except :
                    time.sleep(5)
                    get_link()
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2.0)
                new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
                if new_page_height == last_page_height:
                    time.sleep(2.0)
                    if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                        break
                else:
                    last_page_height = new_page_height
            for i,link in enumerate(tqdm(linkSet)):
                # if i< index_count*howMany:
                #     continue
                
                saveName = f"{inner_page['page_name']}/{link.split('/')[-1].split('?')[0]}"
                urllib.request.urlretrieve(link, saveName)
            index_count += 1
            driver.refresh()
            time.sleep(5)



def infinite_loop(driver):
    #스크롤 내리기
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True: # True
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            time.sleep(1.0)
            if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                break
        else:
            last_page_height = new_page_height