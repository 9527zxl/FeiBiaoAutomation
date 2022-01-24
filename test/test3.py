from selenium import webdriver
import time

from selenium.webdriver.common.by import By


class Crawl_ZhuanLi(object):
    def __init__(self):
        chromeoption = webdriver.ChromeOptions()
        # chromeoption.add_argument('--headless')    # 无头浏览器
        chromeoption.add_argument('--no-sandbox')  # 解决linux DevToolsActivePort文件不存在的报错
        chromeoption.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
        self.driver_path = 'D:\Python 3.10.1\chromedriver.exe'
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=chromeoption)

    def get_value(self, url):
        # 下面这行代码目的为:防止网站识别出是selenium
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.driver.get(url)
        self.driver.implicitly_wait(20)
        time.sleep(20)
        self.driver.find_element(By.XPATH, '//input[@id="username1"]').send_keys('15755188511')
        self.driver.find_element(By.XPATH, '//input[@id="password1"]').send_keys('Zhixin888*')
        time.sleep(60)


Crawl_ZhuanLi().get_value(url='http://cpquery.cnipa.gov.cn/')
