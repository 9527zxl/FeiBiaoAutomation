import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tool.driverTool import driver

driver = driver()
driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)

time.sleep(20)

# hover = driver.find_element(By.XPATH, '//*[@id="selectyzm_text"]')
# ActionChains(driver).move_to_element(hover).perform()

# driver.get_screenshot_as_file('full_screen.png')
