import requests
from urllib.parse import urlencode
from request import WeixinRequest
from db import RedisQueue
from pyquery import PyQuery as pq
from requests import ReadTimeout, ConnectionError
from mysql import MySQL
from config import *


class Spider():
    base_url = 'https://weixin.sogou.com/weixin?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        'Host': 'weixin.sogou.com',
        'Cookie': 'CXID=DC6BC45CC7C377F723DD3A443FE31E4C; SUID=173F49DF3565860A5D15F0D5000657EA; wuid=AAGPCPd4KAAAAAqLFBtmTQ0AGwY=; SUV=008FECF4DF4AD4815D27703DD6AB0621; ABTEST=6|1565489065|v1; IPLOC=CN4451; weixinIndexVisited=1; JSESSIONID=aaaMUF5foWevaeAF9kpXw; sct=3; ppinf=5|1566048243|1567257843|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMTplY2hveHh6aGFuZ3xjcnQ6MTA6MTU2NjA0ODI0M3xyZWZuaWNrOjExOmVjaG94eHpoYW5nfHVzZXJpZDo0NDpvOXQybHVFa1JhOHg0VlN1akEyVWFfWm5jLUlRQHdlaXhpbi5zb2h1LmNvbXw; pprdig=DBBFR2RZZygrUSj6gi2wMUB1mVAlkg1-pTbbkU6YY8rwyrLS6hOyRYi6q8XatVyTLI17Yow3q-RsViuhloTsy7OAJSg2B0PDjiWmSpT53CWn12TzQvcHyhBz9CboxgT-HyjGlyaHZXc5_nX2IY5O8daePYZ5OTh_8FUwTbElygg; sgid=29-42669099-AV1XicicOCeeX2kdrUcM6AiaTo; ppmdig=15660482440000000132fe6a9586fc74c7d7bd1e47980e9d; PHPSESSID=m6o5qn0mr83kplu2nbhu20i2j0; SNUID=3EBF21B46A6EFB3A61BBFA7F6BB0F6F8; successCount=1|Sat, 17 Aug 2019 13:30:39 GMT',
        'Connection': 'keep-alive'
    }
    session = requests.Session()
    queue = RedisQueue()
    mysql = MySQL()

    def get_proxy(self):
        '''
        获取随机代理
        :return: 代理的IP
        '''
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('获取到代理', response.text)
                return response.text
        except requests.ConnectionError:
            print('出错了')
            return None

    def start(self):
        self.session.headers.update(self.headers)  # 更新 headers 参数
        start_url = self.base_url + urlencode(the_dict)  # 拼接url
        weixin_request = WeixinRequest(url=start_url,
                                       callback=self.parse_index, need_proxy=True)

        self.queue.add(weixin_request)
        # 将请求对象添加到队列中

    def parse_index(self, response):
        '''
        解析索引页
        :param response: 响应
        :return: 新的响应
        '''
        doc = pq(response.text)
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            url = item.attr('href')
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            # 列表页的详情页链接
            yield weixin_request
        next = doc('#sogou_next').attr('href')
        if next:
            url = self.base_url + str(next)  # 拼接下一页的URL
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
            # 下一页的详情页链接
            yield weixin_request

    def parse_detail(self, response):
        '''
        解析详情页
        :param response: 响应
        :return: 微信公众号文章
        '''
        doc = pq(response.text)
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    def request(self, weixin_request):
        '''
        执行请求的具体方法
        :param weixin_request:
        :return: 响应
        '''

        try:
            if weixin_request.need_proxy:
                # 实例化对象时，设置是否需要代理,如果是，进入这个控制语句。差别在于是否允许重定向
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http:': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    return self.session.send(weixin_request.prepare(),
                                             timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)

            return self.session.send(weixin_request.prepare(),
                                     timeout=weixin_request.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def error(self, weixin_request):
        '''
        错误处理
        :param weixin_request:
        :return:
        '''
        weixin_request.fail_time = weixin_request.fail_time + 1
        # 增加重试时间
        print('Request Failed', weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            # 如果重试少于最大限制，重新加回对列
            self.queue.add(weixin_request)

    def schedule(self):
        '''
        调度模块
        :return:
        '''
        while not self.queue.empty():  # 如果列表长度不为空
            weixin_request = self.queue.pop()  # 取出一个
            callback = weixin_request.callback
            # callback 被定义为解析列表页的方法

            print(weixin_request.url)
            # print('正在调度:', weixin_request)
            response = self.request(weixin_request)
            print(response)
            if response and response.status_code in VALID_STATUSES:
                results = list(callback(response))
                # 解析列表页
                if results:
                    for result in results:
                        print('New Result', type(result))
                        if isinstance(result, WeixinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('articles', result)
            else:
                # 没有内容，报出错误
                self.error(weixin_request)

    def run(self):
        '''
        函数入口
        :return:
        '''
        self.start()
        self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
