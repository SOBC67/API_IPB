from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_news(region='south'):
    url = f"https://www.thairath.co.th/news/local/{region}"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')

    # webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    time.sleep(2)

    print("✔ เปิดเว็บสำเร็จ")

    articles = driver.find_elements(By.CSS_SELECTOR, "div.css-1r5hw10 a")
    print(f"เจอ {len(articles)} ข่าว")

    for a in articles[::]:  # เอาแค่ 3 ข่าว
        title = a.text.strip()
        link = a.get_attribute("href")
        print(f"หัวข้อ: {title}")
        print(f"ลิงก์: {link}\n")

    driver.quit()

if __name__ == "__main__":
    region = input("ใส่ชื่อภูมิภาค (north/south/east/northeast/central): ").strip()
    get_news(region)
