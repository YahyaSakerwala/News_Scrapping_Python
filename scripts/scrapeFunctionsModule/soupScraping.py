import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from lxml import etree

from scrapeFunctionsModule.mapping import map_categories

def scrape_news(news_links,config_file_path,store_file_path):

    config_path = f"scrape\\config-files\\{config_file_path}"
    store_path=f"scrape\\data\\{store_file_path}"

    with open(config_path, 'r') as file:
                config = json.load(file)



    all_news_jsonArray = []

    for news_link in news_links:
        if news_link is not None:
            response = requests.get(news_link)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser") 

            news_object={}

            for key, value in config.items():

                if value["by"] == "id":
                    element_id = value['id']
                    key_element = soup.find(id=element_id)
                    news_object[key] = key_element.text.strip() if key_element else None

                elif value["by"] == "body":

                    tag = value['tag'] if 'tag' in value else None
                    class_ = value['class'].split() if 'class' in value and value['class'] != "" else []
                    attributes = {attr_key: attr_value for attr_key, attr_value in value['attributes'].items()} if 'attributes' in value and isinstance(value['attributes'], dict) and value['attributes'] else {}

                    if tag is not None and len(class_)==0 and len(attributes)==0:
                        key_element = soup.find(tag)
                        if tag=='meta':
                            news_object[key] = key_element.get('content') if key_element else None
                        else:
                            news_object[key] = key_element.text.strip() if key_element else None

                    if tag is not None and len(class_)!=0 and len(attributes) == 0: 
                        key_element = soup.find(tag, class_=class_)
                        if tag=='meta':
                            news_object[key] = key_element.get('content') if key_element else None
                        else:
                            news_object[key] = key_element.text.strip() if key_element else None

                    if tag is not None and len(class_) ==0 and len(attributes)!=0:
                        key_element = soup.find(tag,attributes)
                        if tag=='meta':
                            news_object[key] = key_element.get('content') if key_element else None
                        else:
                            news_object[key] = key_element.text.strip() if key_element else None
                    
                    if tag is not None and len(class_) !=0 and len(attributes) != 0:
                        key_element = soup.find(tag,class_=class_,attr=attributes)
                        if tag=='meta':
                            news_object[key] = key_element.get('content') if key_element else None
                        else:
                            news_object[key] = key_element.text.strip() if key_element else None
                    
                elif value["by"] == "xpath":
                        soup_lxml = etree.HTML(str(soup))
                        xpath_expression=value['xpath']
                        key_element= soup_lxml.xpath(xpath_expression)
                        news_object[key]=key_element[0].text.strip() if key_element else None

               
            # Map category and add createdTime field
            retrieved_category=news_object['category']
            news_object['category'] = map_categories(retrieved_category) if retrieved_category is not None else "Unknown" 
            news_object['createdTime']=datetime.now().isoformat()
            all_news_jsonArray.append(news_object)
        
        
        with open(store_path, 'w') as json_file:
            json.dump(all_news_jsonArray, json_file, indent=2)