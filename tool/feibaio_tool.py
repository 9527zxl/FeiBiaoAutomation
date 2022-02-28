import json
from time import sleep

import ddddocr
from PIL import Image
from selenium.webdriver import Firefox, ActionChains
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


# 判断元素是否存在
def isElementExist(driver, xpath_path):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath_path)))
        return False
    except:
        return True


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
    # 输入验证码
    driver.find_element(By.XPATH, "//input[@name='captcha']").send_keys(code)
    # 点击登录按钮
    driver.find_element(By.XPATH, "//input[@class='loginin']").click()

    # 判断文字元素存不存在
    def error(xpath, text):
        try:
            WebDriverWait(driver, 2).until(
                EC.text_to_be_present_in_element((By.XPATH, xpath), text))
            return True
        except:
            return False

    # 处理验证码识别错误
    while error(xpath="//div[@class='layui-layer-content']", text='验证码不正确'):
        feibiao_login(username, password)
    # 输入账号密码错误场景
    if error(xpath="//div[@class='layui-layer-content']", text='登录失败，用户名或密码不正确！'):
        driver.quit()
        return '登录失败，用户名或密码不正确！'
    # 等待登录完成
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.XPATH, '//*[@id="LAY_app"]/div[1]/div[2]/div/div/span'), '飞镖网管理后台'))
    # 获取cookies
    cookies_list = json.dumps(driver.get_cookies())

    # 持久化cookies
    with open('../temporary/FeiBiao_Cookies.json', 'w') as f:
        f.write(cookies_list)

    driver.quit()


# 读取并处理飞镖网cookies
def feibiao_cookie():
    with open('../temporary/FeiBiao_Cookies.json', 'r') as f:
        cookies_list = json.load(f)
        cookie = cookies_list[0]['name'] + '=' + cookies_list[0]['value'] + ';' + cookies_list[1]['name'] + '=' + \
                 cookies_list[1]['value']

    return cookie
