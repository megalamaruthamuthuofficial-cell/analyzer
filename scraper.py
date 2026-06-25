from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_reviews(url):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ⚠️ CHANGE THIS PATH IF NEEDED
    service = Service("chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    reviews = []

    try:
        driver.get(url)
        time.sleep(5)

        # 🔥 TRY MULTIPLE SELECTORS (Amazon/Flipkart safe approach)
        elements = driver.find_elements(By.CSS_SELECTOR, "span[data-hook='review-body']")

        # fallback (if Amazon structure changes)
        if not elements:
            elements = driver.find_elements(By.CSS_SELECTOR, ".review-text, .t-ZTKy")

        for el in elements:
            text = el.text.strip()
            if len(text) > 0:
                reviews.append(text)

    except Exception as e:
        print("Scraper error:", e)

    finally:
        driver.quit()

    return reviews