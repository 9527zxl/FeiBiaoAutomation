from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
# 隐藏 正在受到自动软件的控制 这几个字
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

# options.add_argument('--headless')  # 无头浏览器
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
dr = Chrome(options=options)
dr.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
})

dr.get('http://cpquery.cnipa.gov.cn/')
dr.implicitly_wait(20)

input()


