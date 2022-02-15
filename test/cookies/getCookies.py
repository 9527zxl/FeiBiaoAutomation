import json
from selenium import webdriver

driver = webdriver.Firefox()  # Firefox浏览器
driver.get('http://cpquery.cnipa.gov.cn/')

# 程序打开网页后 “手动登陆账户”
input()

with open('cookies.txt', 'w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))

driver.close()
