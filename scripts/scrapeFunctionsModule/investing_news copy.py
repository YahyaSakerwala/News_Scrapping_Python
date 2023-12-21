import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.by import By
from lxml import etree
from datetime import datetime

def scrape_investing_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.investing.com/search/?q=positive%20outlook&tab=news")

    element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".js-section-content.largeTitle:not(.analysisImg)"))
    )

    link_list=[]

    articleItems= element.find_elements(By.CSS_SELECTOR,"div.articleItem")
    for articleItem in articleItems:
        a_element=articleItem.find_element(By.CSS_SELECTOR,"a.img")
        href_link=a_element.get_attribute("href")
        if href_link and href_link not in link_list:
            link_list.append(href_link)

    driver.quit()

    json_data_list = []

 
    for link in link_list:
        if link is not None:
            response = requests.get(link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            with open("config-files\\investing_news_config.json", 'r') as file:
                config = json.load(file)

            metadata={}


            for key, value in config.items():

                if value["by"] == "id":
                    element_id = value['id']
                    key_element = soup.find(id=element_id)
                    metadata[key] = key_element.text.strip() if key_element else None

                elif value["by"] == "body":

                    tag = value['tag'] if 'tag' in value else None
                    class_ = value['class'].split() if 'class' in value else None
                    attributes = {}
                    if 'attributes' in value and isinstance(value['attributes'], dict):
                        attributes = {attr_key: attr_value for attr_key, attr_value in value['attributes'].items()}

                    if tag is not None and class_[0] == 'None' and len(attributes)==0:
                        key_element = soup.find(tag)
                        if tag=='meta':
                            metadata[key] = key_element.get('content') if key_element else None
                        else:
                            metadata[key] = key_element.text.strip() if key_element else None

                    if tag is not None and class_ is not None and len(attributes) == 0: 
                        key_element = soup.find(tag, class_=class_)
                        if tag=='meta':
                            metadata[key] = key_element.get('content') if key_element else None
                        else:
                            metadata[key] = key_element.text.strip() if key_element else None

                    if tag is not None and class_[0] == 'None' and len(attributes)>0:
                        key_element = soup.find(tag,attributes)
                        if tag=='meta':
                            metadata[key] = key_element.get('content') if key_element else None
                        else:
                            metadata[key] = key_element.text.strip() if key_element else None
                    
                    # # have to check over here for attr=attribute
                    # if tag is not None and class_ is not None and isinstance(attributes, dict) and len(attributes) != 0:
                    #     key_element = soup.find(tag,class_=class_,attr=attributes)
                    #     if tag=='meta':
                    #         metadata[key] = key_element.get('content') if key_element else None
                    #     else:
                    #         metadata[key] = key_element.text.strip() if key_element else None
                    
                elif value["by"] == "xpath":
                        soup_lxml = etree.HTML(str(soup))
                        xpath_expression=value['xpath']
                        key_element= soup_lxml.xpath(xpath_expression)
                        metadata[key]=key_element[0].text.strip() if key_element else None

            metadata['createdTime']=datetime.now().isoformat()
            json_data_list.append(metadata)

        with open(os.path.join('data', 'investing_news_copy.json'), 'w') as json_file:
            json.dump(json_data_list, json_file, indent=2)

scrape_investing_news()