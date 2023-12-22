from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapeFunctionsModule.soupScraping import scrape_news

def scrape_ap_news():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('executable_path=C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get("https://apnews.com/search?q=positive+outlook&s=0")

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Link:not(.AnClick-TrendingLink)"))
    )

    news_links = []

    for element in elements:
        href_link = element.get_attribute("href")
        if href_link not in news_links:
            news_links.append(href_link)

    driver.quit()

    config_file_path="ap_news_config.json"
    store_file_path="ap_news.json"
    scrape_news(news_links,config_file_path,store_file_path)

