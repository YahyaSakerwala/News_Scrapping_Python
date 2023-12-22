from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapeFunctionsModule.soupScraping import scrape_news

def scrape_asahi_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()


    driver.get("https://www.asahi.com/ajw/search/results/?keywords=positive+outlook")

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.ID, "SiteSearchResult"))
    )

    news_links = []

    for element in elements:
        a_elements = element.find_elements(By.XPATH, ".//a")
        for a_element in a_elements:
            href_link = a_element.get_attribute("href")
            if href_link and href_link not in news_links:
                news_links.append(href_link)


    driver.quit()
    
    config_file_path="asahi_news_config.json"
    store_file_path="asahi_news.json"
    scrape_news(news_links,config_file_path,store_file_path)
