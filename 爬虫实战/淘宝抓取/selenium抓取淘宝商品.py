from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By   # 导入元素查询
from selenium.webdriver.support import expected_conditions as EC   # 导入条件判断
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote   # 将文字转为url链接呈现的形式
from pyquery import PyQuery as pq
import pymongo


browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)
KEYWORD = 'iPad'

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

MAX_PAGE = 10

def index_page(page):
    print("正在爬取第",page,"页")
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)  # 这样把url写活了，我们只需要更改keyword就可以替换商品信息
        browser.get(url)
        if page >1:   # 如果page大于1,那么就跳页
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#mainsrp-pager div.form > input')))
               # 显示等待：presence_of_element_located表示后面传入的CSS选择器参数的节点存在的话

            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
              '#mainsrp-pager div.form > span.btn.J_Submit')))
               # 表示这个节点是可点击的

            input.clear()          # 将之前的页面数清除
            input.send_keys(page)  # 跳转页面
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                  '#mainsrp-pager li.item.active > span'), str(page)))
        # 判断某个元素中的text是否包含了预期的字符串
        # 这里的意思是，确认当前的页面的页数为我们传入的page值

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   '.m-itemlist .items .item')))
        # 表示商品信息已经加载出来了
        get_products()
    except TimeoutException:
        index_page(page)



def get_products():
    html =  browser.page_source
    doc = pq(html)
    items =  doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print("ok")
    except Exception:
        print("Faild")


def main():
    for i in range(1,MAX_PAGE+1):
        index_page(i)

main()