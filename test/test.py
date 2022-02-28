import json
import random
import re

from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.feibaio_tool import getdriver, isElementExist, feibiao_cookie
from tool.patent_query_tool import account_password, load_verification_code, patent_inquire_code, get_cookies
from tool.patent_update import get_patent_number, patent_update


class code:
    count_code = ''


def login(driver):
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
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@class="tittle_box"]')))

    # 获取登录cookies
    with open('cnipa_cookies.json', 'w') as f:
        # 将cookies保存为json格式
        f.write(json.dumps(driver.get_cookies()))


def click(driver, patent_number):
    url = 'http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?'
    driver.get(url)

    with open('cnipa_cookies.json', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            driver.add_cookie(cookie)

    sleep(2)
    driver.get(url)

    # 检测登录cookies失效
    if exist(driver):
        login(driver)

    # 计算验证码识别,验证码识别错误处理
    def error_code():
        try:
            code.count_code = patent_inquire_code(driver)
            return False
        except Exception:
            return True

    while error_code():
        driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
        # 检测登录cookies失效
        if exist(driver):
            login(driver)
        code.count_code = patent_inquire_code(driver)
    # 请求输入过验证码界面
    driver.get(
        'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
            patent_number) + '&verycode=' + str(
            code.count_code))
    # 检测登录cookies失效
    if exist(driver):
        login(driver)
    # 处理计算验证码失效
    while isElementExist(driver=driver, xpath_path='//*[@class="bi_icon"]'):
        code.count_code = patent_inquire_code(driver)
        driver.get(
            'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + str(
                patent_number) + '&verycode=' + str(
                code.count_code))
        # 检测登录cookies失效
        if exist(driver):
            login(driver)

    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
    # 检测登录cookies失效
    if exist(driver):
        login(driver)
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


# 判断主页面
def exist(driver):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="slogo"]')))
        return True
    except:
        return False


if __name__ == '__main__':
    driver = getdriver()
    driver.get('http://cpquery.cnipa.gov.cn/')
    login(driver)

    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)

    # 获取token
    token = click(driver, patent_number)
    # 获取cookies
    cookies = get_cookies()
    # 更新
    patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)

state = True
while state:
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)

    driver = getdriver()
    click(driver, patent_number)