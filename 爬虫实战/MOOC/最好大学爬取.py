import requests
from bs4 import BeautifulSoup
import bs4
import csv

url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html'
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}


def get_page():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果有错误，则抛出该异常,如果没错误，返回None
        response.encoding = response.apparent_encoding
        html = response.text
        paser_page(html)
    except:
        return ""


def paser_page(html):
    soup = BeautifulSoup(html, 'lxml')
    # result = soup.find_all('tbody')  # 我们发现所有的大学信息都是在tbody这个标签中
    f = open("good.csv", 'w', encoding='utf-8')
    writer = csv.writer(f)
    for tr in soup.find('tbody').children:  # find方法返回的类型依然是 Tag 类型。
        if isinstance(tr, bs4.element.Tag):  # 过滤非标签类型
            td = tr('td')  # 每一个大学所在信息都对应一个 td
            # print(td[0].string,td[1].string,td[3].string)
            daxue, name, paiming = td[0].string, td[1].string, td[3].string
            info_list = [daxue, name, paiming]
            writer.writerow(info_list)


def main():
    get_page()


if __name__ == '__main__':
    main()
