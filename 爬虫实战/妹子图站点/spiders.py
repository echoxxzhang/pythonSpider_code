import requests
from bs4 import BeautifulSoup
import re
import os

class Meizi:
    def __init__(self):
        self.list_url = 'https://www.mzitu.com/all/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
        }
        self.list_dict = []



    def list_page(self):
        response = requests.get(self.list_url, headers=self.headers).content
        content = response.decode('utf-8')

        soup = BeautifulSoup(content, 'lxml')
        all_result = soup.find_all(target="_blank")

        for i in all_result:
            list_dict = {}
            list_dict['title'] = i.get_text()
            list_dict['a'] = i.get('href')
            self.list_dict.append(list_dict)




    def totail(self):
        for i in self.list_dict:
            url = i['a']
            totail_response = requests.get(url, headers=self.headers)
            doc = totail_response.content.decode('utf-8')
            regix = re.compile('<span>(\d+)</span>')
            max_page = regix.findall(doc)[-1]

            for page in range(1, int(max_page) + 1):
                page_url = url + '/' + str(page)
                response = requests.get(page_url, headers=self.headers)
                doc = response.content.decode('utf-8')
                img_Soup = BeautifulSoup(doc, 'lxml')
                img_url = img_Soup.find('div', class_='main-image').find('img')['src']
                # 每个套图实际的图片链接

                self.save(img_url)

        print('爬取完毕')

    def save(self,img_url):
        name = img_url[-9:-4]
        response = requests.get(img_url, headers=self.headers)
        with open(name + '.jpg', 'ab') as f:
            print('正在爬取%s的图片' % name)
            f.write(response.content)

    def start(self):
        self.list_page()
        self.totail()


if __name__ == '__main__':
    m1 = Meizi()
    m1.start()
