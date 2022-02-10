from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
import time

# 配置
from selenium.webdriver.common.by import By

options = ChromeOptions()
# options.add_argument("--headless")  # => 为Chrome配置无头模式
# 隐藏 正在受到自动软件的控制 这几个字
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# 在启动浏览器时加入配置
driver = webdriver.Chrome(options=options)  # => 注意这里的参数
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
})

driver.get("http://cpquery.cnipa.gov.cn/")
driver.implicitly_wait(20)

driver.maximize_window()

input()


