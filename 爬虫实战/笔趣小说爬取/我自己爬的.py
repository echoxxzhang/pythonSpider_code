import urllib.request
from bs4 import BeautifulSoup
from lxml import  etree
import re

url = 'https://www.biqukan.com/1_1094/5403177.html'

def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0','Cookie':'UM_distinctid=16b8523768d317-020cad425c2672-e343166-144000-16b8523768e115; bcolor=; font=; size=; fontcolor=; width=; CNZZDATA1260938422=1245222118-1561302037-https%253A%252F%252Fblog.csdn.net%252F%7C1563150333'}
    Request = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(Request)
    html = response.read()
    return html


def parser_page(html):
    soup = BeautifulSoup(html,'lxml',from_encoding='utf-8')
    text = soup.find('div', class_='showtxt')
    cont = text.get_text()
    cont = str(cont).split()

    print(cont)

if __name__ == '__main__':
    html = get_page(url)
    parser_page(html)