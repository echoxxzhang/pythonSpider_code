import requests
from bs4 import BeautifulSoup


class Clawers():
    def __init__(self):
        self.url = 'https://www.chainnode.com{}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }
        self.data_list = []
        self.totail_list = []

    def get_list_page(self, url):
        response = requests.get(url, headers=self.headers)
        result = response.content
        return result

    def parser_list_page(self, result):
        soup = BeautifulSoup(result, 'lxml')
        list_title = soup.find_all(attrs={'class':'post-item__title'})

        for data in list_title:
            list_dict = {}
            list_dict['title'] = data.get_text().split()   # 列表页中的title
            list_dict['datail_url'] = data.a['href']       # 列表页对应的详情页的 url
            self.data_list.append(list_dict)               # 每一个帖子用一个字典存储，加到列表中

    def parser_totail_page(self,result):
        soup = BeautifulSoup(result, 'lxml')
        totail_len = soup.find_all(attrs={'class': 'header-module__box'})
        answer = soup.find_all(attrs={'class': 'comment__content'})
        totail_dict = {}

        if len(totail_len) > 0:
            totail_title = totail_len[0].get_text().split()
            totail_dict['title'] = totail_title    # 每一个详情页的标题

        the_list = []
        for data in answer:
            the_list.append(data.get_text())
            print('1')

        totail_dict['answer'] = the_list
        self.totail_list.append(totail_dict)

    def save_to_file(self, the_data,file_path):
        with open(file_path + '.txt', 'w', encoding='utf-8') as f:
            f.write(str(the_data) + '\n')

    def run(self):
        for page in range(1,6):
            url = self.url.format('/forum/61-' + str(page))
            data = self.get_list_page(url)
            self.parser_list_page(data)
        self.save_to_file(self.data_list,'list1')

        for the_urls in self.data_list:
            the_url = the_urls['datail_url']
            totail_url = self.url.format(the_url)
            totail_data = self.get_list_page(totail_url)
            self.parser_totail_page(totail_data)
        self.save_to_file(self.totail_list, 'total')


c1 = Clawers()
c1.run()
print(c1.data_list)
print(c1.totail_list)