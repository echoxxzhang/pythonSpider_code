import requests
import json
import time
from pyquery import PyQuery as pq

def req(page):
    url = ' https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv56&productId=45105622340&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1 '%page

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://item.jd.com/45105622340.html'
    }

    response = requests.get(url=url,headers=headers)
    return  response

def xml(response):
    result = response.text[24:-2]
    json_res = json.loads(result)
    comments = json_res['comments']
    return comments


def write(comm):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(comm + '\n')


if __name__ == '__main__':
    for i in range(10):
        response = req(i)
        results = xml(response)

        for result in results:
            content = result['content']
            print(content)
            time.sleep(1)
            write(content)

print("succesful")