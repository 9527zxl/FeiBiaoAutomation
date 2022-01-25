import ddddocr
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


# 识别十已内的加减验证码
def calculate_code(img):
    ocr = ddddocr.DdddOcr()
    with open(img, 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)

    number = list(res.rstrip('='))
    code = 0
    if number[1] == '-':
        code = int(number[0]) - int(number[2])
    elif number[1] == '+':
        code = int(number[0]) + int(number[2])
    return code


def capture_code():
    return
