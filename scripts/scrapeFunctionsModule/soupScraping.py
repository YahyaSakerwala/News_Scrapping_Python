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
from mapping import map_categories
from lxml import etree

def scrape_news(link_list,config_file_path,store_file_path):


    json_data_list = []

 
    for link in link_list:
        if link is not None:
            response = requests.get(link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            config_path = f"config-files\\{config_file_path}"
            with open(config_path, 'r') as file:
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
                        soup_lxml = etree.HTML(str(soup))
                        xpath_expression=value['xpath']
                        key_element= soup_lxml.xpath(xpath_expression)
                        metadata[key]=key_element[0].text.strip() if key_element else None
            
            metadata['createdTime']=datetime.now().isoformat()
            json_data_list.append(metadata)
        
        store_path=f"data\\{store_file_path}"
        with open(store_path, 'w') as json_file:
            json.dump(json_data_list, json_file, indent=2)