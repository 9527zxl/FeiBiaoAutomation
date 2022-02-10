from time import sleep

from selenium.webdriver import ChromeOptions, ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By

options = ChromeOptions()
# 某些网站监控到时selenium就不会返回任何信息，加上词句就可以正常运行了
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--incognito')#无痕模式
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--no-default-browser-check")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
})

driver.get('http://cpquery.cnipa.gov.cn/')

input()

# 定位到要悬停的元素
move = driver.find_element(By.XPATH,'//*[@id="selectyzm_text"]')
# 对定位到的元素执行悬停操作
ActionChains(driver).move_to_element(move).perform()

# driver.find_element(By.XPATH, '//input[@id="username1"]').send_keys('15755188511')
