from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.tool import getdriver

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)
# 显示等待，等待验证码加载出来
WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), u'请依次点击'))

js='window.open("https://www.sogou.com");'
driver.execute_script(js)
driver.switch_to.window(driver.window_handles[1])  # 转到第2个（从0开始）

print(driver.current_url)
