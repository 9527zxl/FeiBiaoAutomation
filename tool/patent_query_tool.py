import gc
import json
import re
from io import BytesIO

import ddddocr
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.feibaio_tool import getdriver, isElementExist


class code:
    count_code = ''


# 专利查询网输入账号密码
def account_password(driver, username, password):
    username_move = driver.find_element(By.XPATH, '//input[@id="username1"]')
    js = 'arguments[0].value= ' + '"' + username + '"' + ';'
    driver.execute_script(js, username_move)
    sleep(0.5)
    password_move = driver.find_element(By.XPATH, '//input[@id="password1"]')
    js = 'arguments[0].value= ' + '"' + password + '"' + ';'
    driver.execute_script(js, password_move)


# 点选验证码验证并点击
def load_verification_code(driver):
    code_text = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text
    data = code_text.split('"')

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
        coord = coord[0], coord[1], coord[2], coord[3]
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

    # 根据坐标点击验证码
    for ss in data:
        for coord_id in code:
            if ss == coord_id['code']:
                ActionChains(driver).move_to_element_with_offset(imgelement, coord_id['X'],
                                                                 coord_id['Y']).click().perform()
                sleep(0.5)

    # 释放内存
    gc.collect()


# 专利查询网计算验证码识别
def patent_inquire_code(driver):
    # 获取计算验证码
    driver.save_screenshot('../temporary/query_page.png')
    imgelement = driver.find_element(By.XPATH, '//*[@id="authImg"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open('../temporary/query_page.png')  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    img = BytesIO()
    frame4.save(img, 'png')  # 保存接下来的验证码图片 进行打码

    ocr = ddddocr.DdddOcr()
    word = ocr.classification(img.getvalue())

    # 对ocr识别后的字符串进行处理
    number = list(word)
    code = 0
    if number[1] == '-':
        code = int(number[0]) - int(number[2])
    elif number[1] == '+':
        code = int(number[0]) + int(number[2])

    gc.collect()
    return code


# 登录专利查询网站根据专利号获取token
def login_patent_inquiry_gettoken(patent_number):
    driver = getdriver()
    driver.get('http://cpquery.cnipa.gov.cn/')
    driver.maximize_window()
    # 隐示等待，用于等待网页加载，应用于全局
    driver.implicitly_wait(20)
    # 显示等待，等待验证码文字加载出来
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), '请依次点击'))
    # 显示等待，等待验证码图片加载出来
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jcaptchaimage"]')))

    # 输入账号密码
    account_password(driver, username='13665695915', password='Zhixin888*')

    # 悬浮验证码图片
    imgyzm = driver.find_element(By.XPATH, '//*[@id="imgyzm"]')
    reload = driver.find_element(By.XPATH, '//*[@id="reload"]')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'style',
                          'position: absolute; bottom: 230px; left: 275px; height: 0px;')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", imgyzm, 'class', 'requestYzm')
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'class', 'refresh')

    load_verification_code(driver)
    # 处理验证码点击错误进行重新加载
    while driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text != '验证成功':
        element = driver.find_element(By.XPATH, '//*[@class="img_reload"]')
        driver.execute_script("arguments[0].click();", element)
        sleep(1)
        load_verification_code(driver)
    else:
        element = driver.find_element(By.XPATH, '//input[@id="publiclogin"]')
        driver.execute_script("arguments[0].click();", element)

    # 等待登录加载完成
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@class="tittle_box"]')))

    # 跳过使用声明，有一定几率加载失败
    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')

    # 计算验证码识别,验证码识别错误处理
    def error_code():
        try:
            code.count_code = patent_inquire_code(driver)
            return False
        except Exception:
            return True

    while error_code():
        driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
        code.count_code = patent_inquire_code(driver)
    # 请求输入过验证码界面
    driver.get(
        'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
            patent_number) + '&verycode=' + str(
            code.count_code))
    # 处理计算验证码失效
    while isElementExist(driver=driver, xpath_path='//*[@class="bi_icon"]'):
        code.count_code = patent_inquire_code(driver)
        driver.get(
            'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
                patent_number) + '&verycode=' + str(
                code.count_code))

    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
    # 等待加载完成
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="jbxx"]/p'), '申请信息'))

    # 通过正则获取token
    token = re.findall('token=(.*?)&', driver.current_url)

    # 将cookies持久化保存
    with open('../temporary/cookies.json', 'w') as f:
        # 将cookies保存为json格式
        f.write(json.dumps(driver.get_cookies()))

    # 退出浏览器
    driver.quit()
    return token[0]


# 根据持久化cookies文件获取cookies
def get_cookies():
    cookie = ''
    with open('../temporary/cookies.json', 'r') as f:
        cookies_list = json.load(f)
        for cookies in cookies_list:
            cookie += cookies['name'] + '=' + cookies['value'] + ';'

    return cookie
