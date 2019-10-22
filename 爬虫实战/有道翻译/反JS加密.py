import hashlib
import time
import random
import requests
import json


def get_sign(salt):
    first = 'fanyideskweb'
    e = KEYWORD
    i = salt
    last = 'n%A-rKaT5fb[Gy?;N5@Tj'
    str_result = first + e + str(i) + last
    md5 = hashlib.md5()
    md5.update(str_result.encode('utf-8'))
    sign = md5.hexdigest()
    return sign


def get_bv():
    version = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
    md5 = hashlib.md5()
    md5.update(version.encode('utf-8'))
    bv = md5.hexdigest()
    return str(bv)


KEYWORD = "pear"
ts = int(time.time() * 1000)
salt = str(ts) + str(random.randint(0, 9))

url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
data = {
    "smartresult": "dict",
    "to": "AUTO",
    "from": "AUTO",
    "doctype": "json",
    "salt": salt,
    "i": KEYWORD,
    "ts": str(ts),
    "sign": get_sign(salt),
    "action": "FY_BY_REALTlME",
    "keyfrom": "fanyi.web",
    "bv": get_bv(),
    "client": "fanyideskweb",
    "version": "2.1"
}

headers = {
    "Cookie": "OUTFOX_SEARCH_USER_ID=1266029150@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=1075804823.494775; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abcY7olcNKLe6b9xzie0w; ___rl__test__cookies=1567748207291",
    "Referer": "http://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}

response = requests.post(url, data=data, headers=headers)

result = json.loads(response.content.decode("utf-8"))
print(result['smartResult']['entries'][1].strip())
