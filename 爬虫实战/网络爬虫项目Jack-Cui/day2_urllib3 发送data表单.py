import urllib.request
import urllib.parse
import json




# req = urllib.request.Request("http://fanyi.baidu.com/")
# #  Request 方法可以构造成一个对象，方便参数添加以及调度
#
# response = urllib.request.urlopen(req)
# html= response.read().decode('U8')
# # urlopen()返回的对象，可以使用read()进行读取，
# # 同样也可以使用geturl()方法、info()方法、getcode()方法。
#
# getinfo =response.info()
# print(getinfo)
# ### 返回META标签，包含网页文档的类型、作者、日期、网页描述等信息

if __name__ == '__main__':
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    # 为什么删掉_o   详看https://blog.csdn.net/li939891142/article/details/84592442

    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        ,'Referer':'http://fanyi.youdao.com/'
    }
    Form_Data = {}     # 构造一个表单
    Form_Data['to'] = 'AUTO'
    Form_Data['i'] = 'Jack'
    Form_Data['doctype'] = 'json'
    Form_Data['version'] = '2.1'
    Form_Data['keyfrom'] = 'fanyi.web'
    Form_Data['action'] = 'FY_BY_REALTlME'

    data = urllib.parse.urlencode(Form_Data).encode('utf-8')
    # 使用urlencode 方法转换标准格式
    req =  urllib.request.Request(headers=headers,url=url)
    response = urllib.request.urlopen(req,data)
    html = response.read().decode('U8')
    # 读取返回的内容
    results = json.loads(html)
    print(results['translateResult'][0][0]['tgt'])


# post 请求就是模仿一个from_data表单