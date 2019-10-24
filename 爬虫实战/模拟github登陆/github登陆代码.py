import requests
from lxml import etree


class Login:
    def __init__(self):
        self.headers = {
            'host': 'github.com',
            'Referer': 'https://github.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        self.login_url = 'https://github.com/login'  # 登陆之前的URL
        self.post_url = 'https://github.com/session'  # 发送POST请求的URL
        self.session = requests.Session()  # 由Session实例化的对象，Cookies会自动保存

    def back_tokenI(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')[0]  # 选中 authenticity_token 参数的值
        return token

    def login(self, username, password):
        data = {
            'commit': 'Sign in',
            'authenticity_token': self.back_tokenI(),
            'utf8': '✓',
            'login': username,
            'password': password
        }
        response = self.session.post(url=self.post_url, headers=self.headers, data=data)
        if response.status_code == 200:
            print('模拟请求成功了！！！')
            return response.text  # 返回登陆成功之后的数据


c1 = Login()
c1.login('username', 'password')
