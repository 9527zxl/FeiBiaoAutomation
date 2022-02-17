import ast
import json
from time import sleep

import cv2
import ddddocr
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tool.tool import getdriver, ddddocr_ocr, inquire_auth_code

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)
sleep(10)
move = driver.find_element(By.XPATH, '//span[@id="selectyzm_text"]')
ActionChains(driver).move_to_element(move).perform()

sleep(2)
driver.save_screenshot("Login.png")
imgelement = driver.find_element(By.XPATH, '//*[@id="jcaptchaimage"]')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
size = imgelement.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open("Login.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取需要的区域
frame4.save('code.png')  # 保存接下来的验证码图片 进行打码

code = inquire_auth_code('code.png')
print(code)

driver.quit()
