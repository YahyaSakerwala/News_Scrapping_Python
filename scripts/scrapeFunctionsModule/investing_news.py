from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapeFunctionsModule.soupScraping import scrape_news

def scrape_investing_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://www.investing.com/search/?q=positive%20outlook&tab=news")

    element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".js-section-content.largeTitle:not(.analysisImg)"))
    )

    news_links=[]

    articleItems= element.find_elements(By.CSS_SELECTOR,"div.articleItem")
    for articleItem in articleItems:
        a_element=articleItem.find_element(By.CSS_SELECTOR,"a.img")
        href_link=a_element.get_attribute("href")
        if href_link and href_link not in news_links:
            news_links.append(href_link)

    driver.quit()

    config_file_path="investing_news_config.json"
    store_file_path="investing_news.json"
    scrape_news(news_links,config_file_path,store_file_path)

