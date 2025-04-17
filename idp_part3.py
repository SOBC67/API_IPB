import requests
from bs4 import BeautifulSoup

url = "https://thairath.co.th/news/local/south"
header = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url,headers=header)

if response.status_code == 200:
    soup = BeautifulSoup(response.text,'html.parser')

    news_section = soup.find_all('div',class_='css-1n9m2d4 e11fmmx12')

    for news in news_section:
        title = news.find('h3').text.strip()
        link = news.find('a')['href']
        print(title)
        print(link)
        print("-"*50)
else:
    print(response.status_code)