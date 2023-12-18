import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.by import By
from datetime import datetime
from scrapeFunctionsModule.mapping import map_categories


def scrape_investing_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.investing.com/search/?q=positive%20outlook&tab=news")

    element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".js-section-content.largeTitle:not(.analysisImg)"))
    )

    href_link_list=[]

    articleItems= element.find_elements(By.CSS_SELECTOR,"div.articleItem")
    for articleItem in articleItems:
        a_element=articleItem.find_element(By.CSS_SELECTOR,"a.img")
        href_link=a_element.get_attribute("href")
        if href_link and href_link not in href_link_list:
            href_link_list.append(href_link)

    driver.quit()

    json_data_list = []

    for link in href_link_list:
        if link is not None:
            response = requests.get(link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            title = soup.find(class_ = "articleHeader").text
            content_section_for_category = soup.find('ul', class_='subNavUL')
            category = content_section_for_category.find(class_ = 'selected').text.strip()
            url = soup.find('meta', property='og:url')
            source = soup.find('meta', property='og:site_name')
            description = soup.find('meta', property='og:description')
            

            metadata = {}

            if title:
                metadata["title"] = title
            else:
                metadata['title'] = None

            if url:
                metadata["url"] = url['content'] 
                metadata["createdDateTime"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                metadata['url'] = None   

            if source:
                metadata["source"] = source['content'] 
            else:
                metadata['source'] = None

            if category:
                metadata["category"] =map_categories(category)
            else:
                metadata["category"] ="Others"
                
            if description:
                metadata["description"] = description['content'] 
            else:
                metadata['description'] = None   

            json_data_list.append(metadata)

    with open(os.path.join('data', 'investing_news.json'), 'w') as json_file:
        json.dump(json_data_list, json_file, indent=2)

