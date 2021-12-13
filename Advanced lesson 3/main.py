from bs4 import BeautifulSoup
import requests

url = 'https://habr.com/ru/all/'
headers = {'User-agent':'Mozilla/5.0'}
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'лидер']

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

articles = soup.findAll('article')
#print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
filtered_articles = []
for article in articles:
    for word in KEYWORDS:
        if word in article.text:
            found = {}
            found['time'] = article.find('time').attrs['title']
            found['href'] = 'https://habr.com' + article.find('a', class_='tm-article-snippet__title-link').attrs['href']
            found['title'] = article.find('a', class_='tm-article-snippet__title-link').text
            print(f"{found['time']} - {found['title']} - {found['href']}")

            
