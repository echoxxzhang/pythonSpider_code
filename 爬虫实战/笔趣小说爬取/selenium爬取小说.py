import selenium
from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.biqukan.com/1_1094/5403177.html'

browser = webdriver.Chrome()
wait = wait.WebDriverWait(browser,10)

browser.get(url)
result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#content')))
print(result.text)
browser.close()