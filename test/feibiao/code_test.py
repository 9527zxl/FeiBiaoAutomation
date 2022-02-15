from time import sleep

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# driver = webdriver.Firefox()  # Firefox浏览器
# driver.get('http://cpquery.cnipa.gov.cn/')
# driver.implicitly_wait(20)
#
# driver.maximize_window()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

data = {
    'type': '1',
    'usertype': '1'
}

url = 'http://cpquery.cnipa.gov.cn/JcaptchaServlet?type=1&usertype=1&date=Tue%20Feb%2015%202022%2016:44:24%20GMT+0800%20(%D6%D0%B9%FA%B1%EA%D7%BC%CA%B1%BC%E4)0.829217005371115'
response = requests.get(url=url,headers=headers)
# 将图片保存
with open("code.png", "wb") as f:
    f.write(response.content)
