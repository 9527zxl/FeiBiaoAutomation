from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

chromeoption = webdriver.ChromeOptions()
# chromeoption.add_argument('--headless')    # 无头浏览器
chromeoption.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
driver_path = 'D:\Python 3.10.1\chromedriver.exe'
driver = webdriver.Chrome(driver_path, chrome_options=chromeoption)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

driver.get('http://cpquery.cnipa.gov.cn/')
driver.implicitly_wait(20)

input()


