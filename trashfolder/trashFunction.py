# from bs4 import BeautifulSoup
# from lxml import etree

# # Example HTML content
# html_content = '''
# <div>
#     <p>Hello, <strong>World!</strong></p>
#     <p>This is an example</p>
# </div>
# '''

# # Create a BeautifulSoup object
# soup = BeautifulSoup(html_content, 'html.parser')

# # Convert BeautifulSoup object to an lxml object
# soup_lxml = etree.HTML(str(soup))

# # Define the XPath expression to find the <strong> tag
# xpath_expression = "/html/body/div[6]/section/div[3]/span[1]

# # Use lxml's xpath method to find elements based on XPath
# result = soup_lxml.xpath(xpath_expression)

# if result:
#     # Get the text of the first found element (if any)
#     element_text = result[0].text.strip()
#     print(element_text)  # Output: World!
# else:
#     print("Element not found")
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
from bs4 import BeautifulSoup
from lxml import etree


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
            soup_lxml = etree.HTML(str(soup))
            xpath_expression = "/html/body/div[6]/section/div[3]/span[1]"
            result = soup_lxml.xpath(xpath_expression)

            if result:
                element_text = result[0].text.strip()
                print(element_text)

scrape_investing_news()