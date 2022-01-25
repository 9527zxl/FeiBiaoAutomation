import json
from time import sleep

import ddddocr
from PIL import Image
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tool.driverTool import calculate_code

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
dr.maximize_window()  # 将浏览器最大化
dr.get('http://cpquery.cnipa.gov.cn/')
dr.implicitly_wait(20)

input()

#  driver.find_element(By.XPATH, '//input[@id="username1"]').send_keys('15755188511')
#  driver.find_element(By.XPATH, '//input[@id="password1"]').send_keys('Zhixin888*')

dr.save_screenshot('printscreen.png')
imgelement = dr.find_element(By.XPATH, '//*[@id="authImg"]')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
size = imgelement.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open("printscreen.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save('code.png')  # 保存我们接下来的验证码图片 进行打码

code = calculate_code()
print(code)

# 输入专利号
dr.find_element(By.XPATH, '//*[@id="select-key:shenqingh"]').send_keys('2020108031465')
sleep(1)
# 输入验证码
dr.find_element(By.XPATH, '//*[@id="very-code"]').send_keys(code)
sleep(1)
# 点击查询
dr.find_element(By.XPATH, '//*[@id="query"]').click()
