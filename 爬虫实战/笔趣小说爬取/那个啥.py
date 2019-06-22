import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://www.biqukan.net/book/23326/9979822.html'
    req  = requests.get(url =url)
    req.encoding ='gbk'
    # print(req.text)
    soup = BeautifulSoup('req','lxml')
    texts = soup.find_all(soup.html.body)
    print(texts)


### 关于这个项目，按照作者的源码以及爬不到了，等以后再说

