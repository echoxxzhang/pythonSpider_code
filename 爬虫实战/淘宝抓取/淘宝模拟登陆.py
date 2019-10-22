import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Taobao_login:
    def __init__(self, username, password):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('disable-infobars')
        # 去掉提示：Chrome正收到自动测试软件的控制
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.url = 'https://login.taobao.com/member/login.jhtml'
        self.browser = webdriver.Chrome(options=chromeOptions)
        self.wait = WebDriverWait(self.browser, 10)  # 等待的超时时间
        self.username = username
        self.password = password

    def login(self):
        self.browser.get(url=self.url)

        clickable_password_login = '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static'
        login_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, clickable_password_login)))
        # 切换密码登录
        login_button.click()

        weibo_login = '#J_OtherLogin > a.weibo-login'

        login_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, weibo_login)))
        # 切换密码登录
        login_button.click()

        # 用户名输入框
        usename_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(2) > div > input')))
        # 密码输入框
        password_botton = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(3) > div > input')))

        usename_button.send_keys(self.username)
        password_botton.send_keys(self.password)

        # 登陆按钮
        click_login = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#pl_login_logged > div > div:nth-child(7) > div:nth-child(1) > a > span')))
        click_login.click()

        # 此时碰上了验证码。。。

taobao = Taobao_login('13715742522', 'zzh3915800')
taobao.login()
