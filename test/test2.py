from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.tool import getdriver

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)
# 显示等待，等待验证码文字加载出来
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), '请依次点击'))
# 显示等待，等待验证码图片加载出来
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jcaptchaimage"]')))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="img_reload"]')))
