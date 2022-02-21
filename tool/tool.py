import gc
import json
from io import BytesIO
from time import sleep

import ddddocr
from PIL import Image
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By


def getdriver():
    options = FirefoxOptions()
    options.add_argument('--headless')  # 无头浏览器
    driver_path = 'D:\PythonWarehouse\FeiBiaoAutomation\driver\geckodriver.exe'
    driver = Firefox(executable_path=driver_path, options=options)

    return driver


# ddddocr_ocr验证码识别
def ddddocr_ocr(img_location):
    ocr = ddddocr.DdddOcr()
    with open(img_location, 'rb') as f:
        img_bytes = f.read()
    code = ocr.classification(img_bytes)
    return code


# 专利查询网计算验证码识别
def patent_inquire_code(driver):
    # 验证码地址
    url = 'http://cpquery.cnipa.gov.cn/freeze.main?txn-code=createImgServlet'
    driver.get(url)
    driver.save_screenshot('../temporary/calculate.png')
    rangle = 648, 328, (648 + 70), (328 + 20)  # 写成我们需要截取的位置坐标
    i = Image.open('../temporary/calculate.png')  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取需要的区域
    img_byte = BytesIO()
    frame4.save(img_byte, 'png')
    # 识别单个图片
    ocr = ddddocr.DdddOcr()
    img = ocr.classification(img_byte.getvalue())

    # 对ocr识别后的字符串进行处理
    number = list(img)
    code = 0
    if number[1] == '-':
        code = int(number[0]) - int(number[2])
    elif number[1] == '+':
        code = int(number[0]) + int(number[2])

    gc.collect()
    return code


# 登录飞镖网后台获取cookies值
def feibiao_login(username, password):
    driver = getdriver()
    driver.get('http://www.ipfeibiao.com/manager/frame/index')
    driver.maximize_window()
    driver.implicitly_wait(20)

    # 定位元素输入账号密码
    driver.find_element(By.XPATH, "//input[@name='user_name']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)

    # 获取验证码
    driver.save_screenshot('../temporary/FeiBiao_Login.png')
    imgelement = driver.find_element(By.XPATH, '//*[@id="img_captcha"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open("../temporary/FeiBiao_Login.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('../temporary/FeiBiao_Code.png')  # 保存我们接下来的验证码图片 进行打码

    # 识别验证码
    code = ddddocr_ocr('../temporary/FeiBiao_Code.png')

    driver.find_element(By.XPATH, "//input[@name='captcha']").send_keys(code)

    driver.find_element(By.XPATH, "//input[@class='loginin']").click()

    cookies_list = json.dumps(driver.get_cookies())

    # 持久化cookies
    with open('../temporary/FeiBiao_Cookies.txt', 'w') as f:
        f.write(cookies_list)


# 读取并处理飞镖网cookies
def feibiao_cookie():
    with open('../temporary/FeiBiao_Cookies.txt', 'r') as f:
        cookies_list = json.load(f)
        cookie = cookies_list[0]['name'] + '=' + cookies_list[0]['value'] + ';' + cookies_list[1]['name'] + '=' + \
                 cookies_list[1]['value']

    return cookie


# 专利查询网输入账号密码
def login_patent_inquiry(driver, username, password):
    username_move = driver.find_element(By.XPATH, '//input[@id="username1"]')
    js = 'arguments[0].value= ' + '"' + username + '"' + ';'
    driver.execute_script(js, username_move)
    sleep(0.5)
    password_move = driver.find_element(By.XPATH, '//input[@id="password1"]')
    js = 'arguments[0].value= ' + '"' + password + '"' + ';'
    driver.execute_script(js, password_move)


# 定位验证码并点击
def Load_verification_code(driver):
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
    # 根据坐标点击验证码
    for ss in data:
        for coord_id in code:
            if coord_id['code'] == ss:
                ActionChains(driver).move_to_element_with_offset(imgelement, coord_id['X'],
                                                                 coord_id['Y']).click().perform()
                sleep(1)

    # 释放内存
    gc.collect()

    print(code)
    print(data)
