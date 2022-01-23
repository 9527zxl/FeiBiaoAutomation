from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions


def driver():
    options = ChromeOptions()
    # options.add_argument('--headless')    # 无头浏览器
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
    return dr


def gain_patent_number():
    return
