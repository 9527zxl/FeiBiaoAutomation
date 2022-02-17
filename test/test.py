import ast
import json
from time import sleep

import cv2
import ddddocr
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tool.tool import getdriver, ddddocr_ocr

# driver = getdriver()
#
# driver.get('http://cpquery.cnipa.gov.cn/')
# driver.maximize_window()
# driver.implicitly_wait(20)
# sleep(2)
# move = driver.find_element(By.XPATH, '//span[@id="selectyzm_text"]')
# ActionChains(driver).move_to_element(move).perform()
#
# sleep(2)
# driver.save_screenshot("Login.png")
# rangle = (798, 226, 798 + 308, 226 + 218)
# i = Image.open("Login.png")  # 打开截图
# frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取需要的区域
# frame4.save('code.png')  # 保存接下来的验证码图片 进行打码

det = ddddocr.DdddOcr(det=True)

with open("code.png", 'rb') as f:
    image = f.read()
poses = det.detection(image)
# print(poses)

code = []
count = 0
for coord in poses:
    count += 1
    rangle = (coord[0], coord[1], coord[2], coord[3])
    i = Image.open("code.png")
    frame4 = i.crop(rangle)
    name = 'code-' + str(count) + '.png'
    frame4.save(name)

    ocr = ddddocr_ocr(name)
    # print(tuple(ocr)+rangle)
    # code.append(tuple(ocr)+rangle)
    t = str(rangle[0]) + ',' + str(rangle[1])
    json = '{"' + 'code' + '": ' + '"' + ocr + '","' + 'x' + '": ' + '"' + str(
        rangle[0]) + '","' + 'Y' + '": ' + '"' + str(rangle[1]) + '"}'

    code.append(json)

print(code[0])

