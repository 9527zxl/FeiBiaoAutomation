import json
import re

from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.tool import getdriver, login_patent_inquiry, patent_inquire_code, load_verification_code

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)
# 显示等待，等待验证码加载出来
WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), u'请依次点击'))

# 输入账号
login_patent_inquiry(driver, username='15156052212', password='Zhixin888*')

move = driver.find_element(By.XPATH, '//span[@id="selectyzm_text"]')
ActionChains(driver).move_to_element(move).perform()
sleep(1)

load_verification_code(driver)
WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@class="tittle_box"]')))

elementObj = driver.find_element(By.XPATH, '//*[@id="goBtn"]')
driver.execute_script("arguments[0].removeAttribute(arguments[1])", elementObj, 'disabled')
sleep(2)
elementObj.click()
# driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')

# token = re.findall('token=(.*?)&', driver.current_url)
# print(token)
# with open('../temporary/cookies.json', 'w') as f:
#     # 将cookies保存为json格式
#     f.write(json.dumps(driver.get_cookies()))
# cookie = ''
# with open('../temporary/cookies.json', 'r') as f:
#     cookies_list = json.load(f)
#     for cookies in cookies_list:
#         cookie += cookies['name'] + '=' + cookies['value'] + ';'
# print(cookie)
#
# driver.quit()
