import gc
from io import BytesIO
from time import sleep

import ddddocr
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tool.tool import getdriver

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)
sleep(10)
move = driver.find_element(By.XPATH, '//span[@id="selectyzm_text"]')
ActionChains(driver).move_to_element(move).perform()
sleep(2)

driver.save_screenshot('../temporary/patent_inquire_login.png')

imgelement = driver.find_element(By.XPATH, '//*[@id="jcaptchaimage"]')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
size = imgelement.size  # 获取验证码的长宽
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open('../temporary/patent_inquire_login.png')  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取需要的区域
img_byte = BytesIO()
frame4.save(img_byte, 'png')  # 保存接下来的验证码图片 进行打码

det = ddddocr.DdddOcr(det=True)
poses = det.detection(img_byte.getvalue())
print(poses)

code = []
for coord in poses:
    coord = (coord[0], coord[1], coord[2], coord[3])

    img_base = Image.open(BytesIO(img_byte.getvalue()))

    frame = img_base.crop(coord)  # 使用Image的crop函数，从截图中再次截取需要的区域
    img = BytesIO()
    frame.save(img, 'png')  # 保存图片

    # 识别单个图片
    ocr = ddddocr.DdddOcr()
    word = ocr.classification(img.getvalue())

    # 根据四个坐标计算中心点
    a = dict(code=word, X=int((coord[0] + coord[2]) / 2), Y=int((coord[1] + coord[3]) / 2))
    code.append(a)

code_text = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text
data = code_text.split('"')

for ss in data:
    for coord_id in code:
        if coord_id['code'] == ss:
            ActionChains(driver).move_to_element_with_offset(imgelement, coord_id['X'],
                                                             coord_id['Y']).click().perform()
            sleep(1)

gc.collect()
driver.save_screenshot('./aa.png')
driver.quit()
print(code)
print(data)
