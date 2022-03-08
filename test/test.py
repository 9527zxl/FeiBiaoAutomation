import gc
import json
import random
import re
from io import BytesIO

import ddddocr
from PIL import Image
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.feibaio_tool import getdriver, feibiao_cookie
from tool.patent_query_tool import gettoken
from tool.patent_update import get_patent_number, patent_update, update_successfully


class code:
    count_code = ''


# 判断元素是否存在
def does_the_element_exist(driver, xpath_path, time):
    try:
        WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath_path)))
        return True
    except:
        return False


# 判断文字是否存在，如果不是则退出
def whether_words_exist(driver, xpath_path, time, content):
    try:
        WebDriverWait(driver, time).until(EC.text_to_be_present_in_element((By.XPATH, xpath_path), content))
        return True
    except:
        return False


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
                try:
                    ActionChains(driver).move_to_element_with_offset(imgelement, coord_id['X'],
                                                                     coord_id['Y']).click().perform()
                    sleep(0.5)
                except Exception:
                    pass

    # 释放内存
    gc.collect()


# 专利查询网计算验证码识别
def patent_inquire_code(driver):
    # 获取计算验证码
    driver.save_screenshot('../temporary/query_page.png')

    # 处理定位验证码失败
    if not does_the_element_exist(driver=driver, xpath_path='//*[@id="authImg"]', time=2):
        driver.refresh()
        patent_inquire_code(driver)

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


# 登录专利查询网站
def login(username, password):
    driver = getdriver()
    driver.get('http://cpquery.cnipa.gov.cn/')
    driver.maximize_window()
    # 隐示等待，用于等待网页加载，应用于全局
    driver.implicitly_wait(20)

    # 解决网站加载超时问题
    if not whether_words_exist(driver=driver, xpath_path='//*[@id="selectyzm_text"]', time=20, content='请依次点击'):
        driver.quit()
        login(username, password)

    # 显示等待，等待验证码图片加载出来
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jcaptchaimage"]')))

    # 输入账号密码
    account_password(driver, username=username, password=password)

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
    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@class="tittle_box"]'), '使用声明'))


# 根据持久化cookies文件获取cookies
def get_cookies():
    cookie = ''
    with open('../temporary/cookies.json', 'r') as f:
        cookies_list = json.load(f)
        for cookies in cookies_list:
            cookie += cookies['name'] + '=' + cookies['value'] + ';'

    return cookie


# 流程
def process(patent_number):
    driver = getdriver()
    # 进入查询页面
    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
    # 等待加载完成
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@class="tab_top_on"]/p'), '案件信息查询'))
    # 等待验证码加载完成
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="authImg"]')))
    # 进行验证码识别
    code.count_code = patent_inquire_code(driver)
    # 请求输入过验证码界面
    driver.get(
        'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
            patent_number) + '&verycode=' + str(
            code.count_code))
    # 处理计算验证码失效
    while not does_the_element_exist(driver=driver, xpath_path='//*[@class="bi_icon"]', time=0):
        code.count_code = patent_inquire_code(driver)
        driver.get(
            'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
                patent_number) + '&verycode=' + str(
                code.count_code))

    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
    # 等待加载完成
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="jbxx"]/p'), '申请信息'))
    # 通过正则获取token
    token = re.findall('token=(.*?)&', driver.current_url)
    # 将cookies持久化保存
    with open('../temporary/cookies.json', 'w') as f:
        # 将cookies保存为json格式
        f.write(json.dumps(driver.get_cookies()))
    return token[0]


if __name__ == '__main__':
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)
    print('专利号:' + str(patent_number))
    # 登录
    login()
    # 获取token
    token = process(patent_number)
