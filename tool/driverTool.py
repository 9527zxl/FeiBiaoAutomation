from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def driver():
    options = Options()
    # chrome.exe --remote-debugging-port=9527 --user-data-dir=“E:\Chrome”
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    return webdriver.Chrome(options=options)