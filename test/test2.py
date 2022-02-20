from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tool.tool import getdriver

driver = getdriver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.implicitly_wait(20)
WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="selectyzm_text"]'), u'请依次点击'))

text = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text
# ActionChains(driver).move_to_element(text).perform()

print(text)
input()
aa = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]').text
print(aa)

driver.quit()
