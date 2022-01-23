from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    options = Options()
    # chrome.exe --remote-debugging-port=9527 --user-data-dir=“D:\Chrome”
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    bro = webdriver.Chrome(options=options)

    bro.get('http://cpquery.cnipa.gov.cn/')
    bro.implicitly_wait(20)
    sleep(3)

    bro.find_element(By.XPATH, '//input[@id="username1"]').send_keys('15755188511')
    bro.find_element(By.XPATH, '//input[@id="password1"]').send_keys('Zhixin888*')

    input()

    bro.find_element(By.XPATH, '//input[@id="publiclogin"]').click()
    cookis = bro.get_cookies()
    print(cookis)
