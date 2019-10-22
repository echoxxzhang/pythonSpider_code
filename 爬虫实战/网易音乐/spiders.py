import requests
from bs4 import BeautifulSoup

url = 'https://music.163.com/#/discover/playlist/'

headers= {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

response = requests.get(url=url,headers=headers)
print(response.content.decode('utf-8'))
