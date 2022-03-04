import json
import random
import re
import time

from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.feibaio_tool import getdriver, feibiao_cookie
from tool.patent_query_tool import account_password, load_verification_code, patent_inquire_code, get_cookies
from tool.patent_update import get_patent_number, patent_update


class code:
    count_code = ''


def login():
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
    account_password(driver, username='18656758970', password='Zhixin888*')
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
    # 进入查询页面
    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
    driver.implicitly_wait(10)
    # 获取登录cookies
    dictCookies = driver.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
    with open('../temporary/cnipa_cookies.text', 'w') as f:
        # 将cookies保存为json格式
        f.write(jsonCookies)
    driver.quit()


def click():
    driver = getdriver()
    driver.get('http://cpquery.cnipa.gov.cn/')
    driver.maximize_window()
    # 隐示等待，用于等待网页加载，应用于全局
    driver.implicitly_wait(20)

    # 首先清除由于浏览器打开已有的cookies
    driver.delete_all_cookies()

    with open('../temporary/cnipa_cookies.text', 'r', encoding='utf8') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        listCookies = json.loads(f.read())

    # 往driver里添加cookies
    for cookie in listCookies:
        cookie_dict = {
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'path': '/',
            'domain': cookie.get('domain'),
        }
        driver.add_cookie(cookie_dict)

    driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')


# login()

click()
