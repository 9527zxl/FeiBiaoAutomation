from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


def driver():
    options = Options()
    # chrome.exe --remote-debugging-port=9527 --user-data-dir=“E:\Chrome”
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    bro = Chrome(options=options)
    bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    return bro


def pages(page):
    return driver().switch_to_window(driver().window_handles[page])


class Patent:
    pass
