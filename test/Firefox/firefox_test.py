from time import sleep

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By

# options = FirefoxOptions()
# options.add_argument('--headless')  # 无头浏览器
# driver = Firefox(options=options)

driver = webdriver.Firefox()  # Firefox浏览器
driver.get('http://cpquery.cnipa.gov.cn/')

driver.implicitly_wait(20)

username = driver.find_element(By.XPATH, '//input[@id="username1"]')
js = "arguments[0].value= '15755188511';"
driver.execute_script(js, username)

password = driver.find_element(By.XPATH, '//input[@id="password1"]')
js = "arguments[0].value= 'Zhixin888*';"
driver.execute_script(js, password)
