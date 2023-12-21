import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from news_json import get_news_json
from datetime import datetime
from mapping import map_categories

# ELASTIC_PASSWORD = "OMddL2qDGNJinws6DnNq"
# index_name="ap_news"

# client = Elasticsearch(
#     "https://localhost:9200",
#     ca_certs="C:\\Users\\3439\\Elastic-Kibana\\kibana-8.11.3\\data\\ca_1702534907563.crt",
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )

# print(client.ping())


def scrape_ap_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://apnews.com/search?q=positive+outlook&s=0")

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Link:not(.AnClick-TrendingLink)"))
    )

    link_list = []

    for element in elements:
        href_link = element.get_attribute("href")
        if href_link not in link_list:
            link_list.append(href_link)

    driver.quit()

    json_data_list = []

 
    for link in link_list:
        if link is not None:
            response = requests.get(link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")

            with open("config-files\\ap_news.json", 'r') as file:
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

                    if tag is not None and class_[0] == 'None':
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
                        print("user selected xpath")
            

            json_data_list.append(metadata)

        with open(os.path.join('data', 'ap_news_copy.json'), 'w') as json_file:
            json.dump(json_data_list, json_file, indent=2)
scrape_ap_news()