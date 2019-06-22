import urllib.request
import chardet    # 获取网页编码的库

# response = urllib.request.urlopen('http://www.baidu.com')
# html = response.read().decode('U8')
# # response 返回的是字节流，使用utf-8进行解码
# print(html)

response = urllib.request.urlopen('http://www.baidu.com')
html = response.read()
charset =  chardet.detect(html)   # 解析代码，返回一个字典，包含编码类型等信息
print(html.decode(charset['encoding']))