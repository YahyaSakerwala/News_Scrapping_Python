import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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

            title = soup.find('meta', property='og:title')
            url = soup.find('meta', property='og:url')
            description = soup.find('meta', property='og:description')
            publishedDateTime = soup.find('meta', property='article:published_time')
            category = soup.find('meta', property='article:section')
            newsSource = soup.find('meta', property='og:site_name')

            metadata = {}

            if title:
                metadata["title"] = title['content']
            else:
                metadata['title'] = None

            if url:
                metadata["url"] = url['content']
            else:
                metadata["url"] = None

            if category:
                metadata["category"] = category['content']
            else:
                metadata["category"] = None

            if newsSource:
                metadata["newsSource"] = newsSource['content']
            else:
                metadata["newsSource"] = None

            if description:
                metadata["description"] = description['content']
            else:
                metadata["description"] = None

            if publishedDateTime:
                metadata["publishedDateTime"] = publishedDateTime['content']
            else:
                metadata["publishedDateTime"] = None

            json_data_list.append(metadata)

    with open(os.path.join('data', 'ap_news.json'), 'w') as json_file:
        json.dump(json_data_list, json_file, indent=2)

# if __name__ == "__main__":
#     scrape_apnews_data()


# with open("data/apnews_data.json","r") as f:
#     json_objects = json.load(f)
#     f.close() 

# # creating a index 
# client.indices.create(index="ap_news")
 
# for json_doc in json_objects:
#     doc_id=json_doc['url']
#     response = client.index(index=index_name, body=json_doc, id=doc_id)