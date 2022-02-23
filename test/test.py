# import json
# import re
#
# from selenium.webdriver.support import expected_conditions as EC
# from time import sleep
#
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
#
# from tool.tool import getdriver, login_patent_inquiry, patent_inquire_code, load_verification_code, isElementExist
#
# driver = getdriver()
# driver.get('http://cpquery.cnipa.gov.cn/')
# driver.maximize_window()
# # 隐示等待，用于等待网页加载，应用于全局
# driver.implicitly_wait(20)
# # 显示等待，等待验证码文字加载出来
# WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), '请依次点击'))
# # 显示等待，等待验证码图片加载出来
# WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jcaptchaimage"]')))
#
# # 输入账号密码
# login_patent_inquiry(driver, username='15156052212', password='Zhixin888*')
#
# # 悬浮验证码图片
# imgyzm = driver.find_element(By.XPATH, '//*[@id="imgyzm"]')
# reload = driver.find_element(By.XPATH, '//*[@id="reload"]')
# driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'style',
#                       'position: absolute; bottom: 230px; left: 275px; height: 0px;')
# driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", imgyzm, 'class', 'requestYzm')
# driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", reload, 'class', 'refresh')
#
# load_verification_code(driver)
# # 处理验证码点击错误进行重新加载
# while driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text != '验证成功':
#     element = driver.find_element(By.XPATH, '//*[@class="img_reload"]')
#     ActionChains(driver).move_to_element_with_offset(element, 15, 15).click().perform()
#     sleep(2)
#     load_verification_code(driver)
# else:
#     driver.find_element(By.XPATH, '//input[@id="publiclogin"]').click()
#
# # 等待登录加载完成
# WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@class="tittle_box"]')))
#
# driver.get('http://cpquery.cnipa.gov.cn/txnPantentInfoList.do?')
# # 计算验证码识别
# count_code = patent_inquire_code(driver)
# driver.get(
#     'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + '2017107806169' + '&verycode=' + str(
#         count_code))
# # 处理计算验证码失效或识别错误
# # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@class="bi_icon"]')))
# while isElementExist(driver=driver, xpath_path='//*[@class="bi_icon"]'):
#     count_code = patent_inquire_code(driver)
#     driver.get(
#         'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=' + '2017107806169' + '&verycode=' + str(
#             count_code))
#
# driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[2]/div/ul/li[1]/a').click()
#
# token = re.findall('token=(.*?)&', driver.current_url)
# print(token[0])
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
