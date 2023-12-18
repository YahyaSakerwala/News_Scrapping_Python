import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from elasticsearch import Elasticsearch
from datetime import datetime
from scrapeFunctionsModule.mapping import map_categories



def scrape_asahi_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.asahi.com/ajw/search/results/?keywords=positive+outlook")

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.ID, "SiteSearchResult"))
    )

    href_list = []

    for element in elements:
        a_elements = element.find_elements(By.XPATH, ".//a")
        for a_element in a_elements:
            href_link = a_element.get_attribute("href")
            if href_link and href_link not in href_list:
                href_list.append(href_link)


    driver.quit()

    json_data_list = []

    for link in href_list:
        if link is not None:
            response = requests.get(link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")            

            title = soup.find('meta', property='og:title')
            url = soup.find('meta', property='og:url')
            description = soup.find('meta', property='og:description')
            # publishedDateTime = soup.find('p', class_='EnLastUpdated').text
            category = soup.find('p', class_='Genre').text
            newsSource = soup.find('meta', property='og:site_name')
            

            metadata = {}

            if title:
                metadata["title"] = title['content']
            else:
                metadata['title'] = None

            if url:
                metadata["url"] = url['content']
                metadata["createdDateTime"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                metadata['url'] = None

            if category:
                metadata["category"] =map_categories(category)
            else:
                metadata["category"] ="Others"

            if newsSource:
                metadata["newsSource"] = newsSource['content']
            else:
                metadata['newsSource'] = None

            if description:
                metadata["description"] = description['content']
            else:
                metadata['description'] = None

            # if publishedDateTime:
            #     metadata["publishedDateTime"]=publishedDateTime
            # else:
            #     metadata['publishedDateTime'] = None

            json_data_list.append(metadata)

    with open(os.path.join('data', 'asahi_news.json'), 'w') as json_file:
        json.dump(json_data_list, json_file, indent=2)