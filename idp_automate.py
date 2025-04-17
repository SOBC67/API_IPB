from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_new(region):
    url = f"https://www.thairath.co.th/news/local/{region}"

    driver = webdriver.Chrome()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(options=options)

    #driver recieve url
    driver.get(url)
    time.sleep(2)

    #find news from 1st place
    articles = driver.find_elements(By.CSS_SELECTOR,"div.css-1r5hw10 a")
    news_data = []

    for a in articles[:1]:
        #get title
        title = a.text.strip()
        #get link
        link = a.get_attribute("href")

        #go to news
        driver.get(link)
        time.sleep(1)

        #body news
        try:
            content = driver.find_element(By.CLASS_NAME, "css-nh9sg4")
            paragraphs = content.find_elements(By.TAG_NAME, 'p')
            contents = '\n'.join(p.text for p in paragraphs)
        except:
            contents = ''

        news_data.append({
            'title': title,
            'url' : link,
            'content' : contents
        })

        driver.back()
        time.sleep(1)

    driver.quit()
    return news_data

region = input("what region do you want to know news? :")
news_list = get_new(region)
for news in news_list:
    print(news["title"])
    print(news['url'])
    print(news['content'])
        

