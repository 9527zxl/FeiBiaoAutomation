import time
from selenium import webdriver
import json

# 填写webdriver的保存目录
driver = webdriver.Firefox()
url = 'http://cpquery.cnipa.gov.cn/txnDisclaimerDetail.do?select-key:yuzhong=zh&select-key:gonggaolx=3'

# 记得写完整的url 包括http和https
driver.get(url)

# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()

with open('cookies.txt', 'r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)

time.sleep(3)
# driver.refresh()
driver.get(url)
