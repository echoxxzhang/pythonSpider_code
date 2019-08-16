import re
import requests


url ='https://i.meizitu.net/2019/06/23c06.jpg'

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
        }

response = requests.get(url,headers=headers)
doc = response.content
with open('test.jpg','wb') as f:
    f.write(doc)
