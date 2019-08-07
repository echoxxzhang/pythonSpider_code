### 由于网页被md5加密，换成selenium进行抓取

import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


KEYWORD = '无语'
browser = webdriver.Chrome()
url = 'http://fanyi.youdao.com'
wait = WebDriverWait(browser,10)

browser.get(url)
input = wait.until(EC.presence_of_element_located
                   ((By.CSS_SELECTOR , '#inputOriginal')))
input.send_keys(KEYWORD)

result = wait.until(EC.presence_of_element_located
                    ((By.CSS_SELECTOR,'#transTarget > p > span')))

print(KEYWORD,"==>翻译的结果是：",result.text)
browser.close()