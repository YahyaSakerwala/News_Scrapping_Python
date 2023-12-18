from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def scrape_bloomberg_news():
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("C:\\Users\\3439\\python_scrapping\\drivers\\chromedriver.exe")

    driver=webdriver.Chrome(options=chrome_options)
    driver.maximize_window
    driver.get("https://www.bloomberg.com/search?query=positive%20outlook")

    elements= WebDriverWait(driver,20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,".storyItem__aaf871c1c5"))
    )
    

scrape_bloomberg_news()