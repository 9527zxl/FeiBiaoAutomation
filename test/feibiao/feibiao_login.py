import json

import muggle_ocr
from PIL import Image
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

options = ChromeOptions()
# options.add_argument('--headless')  # 无头浏览器
driver = Chrome(options=options)

driver.get('http://www.ipfeibiao.com/manager/frame/index')
driver.maximize_window()
driver.implicitly_wait(20)

driver.find_element(By.XPATH, "//input[@name='user_name']").send_keys('zhuxingli')
driver.find_element(By.XPATH, "//input[@name='password']").send_keys('zhuxingli')

driver.save_screenshot('./code/FeiBiaoLogin.png')
imgelement = driver.find_element(By.XPATH, '//*[@id="img_captcha"]')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
size = imgelement.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open("./code/FeiBiaoLogin.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save('./code/code.png')  # 保存我们接下来的验证码图片 进行打码

# 初始化sdk；model_type 包含了 ModelType.OCR/ModelType.Captcha 两种模式,分别对应常规图片与验证码
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
with open(r"./code/code.png", "rb") as f:
    img = f.read()
code = sdk.predict(image_bytes=img)
print(code)

driver.find_element(By.XPATH, "//input[@name='captcha']").send_keys(code)

driver.find_element(By.XPATH, "//input[@class='loginin']").click()

cookie = json.dumps(driver.get_cookies())

print(cookie)






