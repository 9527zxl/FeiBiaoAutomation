from time import sleep

from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tool.tool import getdriver

driver = getdriver()

driver.get('http://cpquery.cnipa.gov.cn/')
driver.maximize_window()
driver.implicitly_wait(20)

sleep(15)

move = driver.find_element(By.XPATH, '//span[@id="selectyzm_text"]')
ActionChains(driver).move_to_element(move).perform()

sleep(2)
driver.save_screenshot("Login.png")
rangle = (1057, 286, 1057 + 387, 286 + 273)
i = Image.open("Login.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save('code.png')  # 保存我们接下来的验证码图片 进行打码
