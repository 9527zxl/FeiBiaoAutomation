import json

import ddddocr
import requests
from PIL import Image
from selenium.webdriver import Firefox
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
def patent_inquire_code(img_location):
    # 验证码地址
    url = 'http://cpquery.cnipa.gov.cn/freeze.main?txn-code=createImgServlet'
    response = requests.get(url)
    # 将图片保存
    with open(img_location, "wb") as f:
        f.write(response.content)

    # 验证码识别
    img = ddddocr_ocr(img_location)

    # 对ocr识别后的字符串进行处理
    number = list(img)
    code = 0
    if number[1] == '-':
        code = int(number[0]) - int(number[2])
    elif number[1] == '+':
        code = int(number[0]) + int(number[2])

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


# # 读取并处理飞镖网cookies
def feibiao_cookie():
    with open('../temporary/FeiBiao_Cookies.txt', 'r') as f:
        cookies_list = json.load(f)
        cookie = cookies_list[0]['name'] + '=' + cookies_list[0]['value'] + ';' + cookies_list[1]['name'] + '=' + \
                 cookies_list[1]['value']

    return cookie


# 处理查询网站点选验证码
def inquire_auth_code(img_location):
    det = ddddocr.DdddOcr(det=True)

    # 读取验证码并返回坐标
    with open(img_location, 'rb') as f:
        image = f.read()
    poses = det.detection(image)

    code = []
    count = 0
    for coord in poses:
        count += 1
        coord = (coord[0], coord[1], coord[2], coord[3])
        i = Image.open(img_location)
        frame4 = i.crop(coord)
        # 扣除文字图片并重命名保存
        name = '../temporary/patent_Login_code-' + str(count) + '.png'
        frame4.save(name)

        ocr = ddddocr_ocr(name)
        t = str(coord[0]) + ',' + str(coord[1])

        a = dict(code=ocr, X=coord[0], Y=coord[1])

        code.append(a)

    return code
