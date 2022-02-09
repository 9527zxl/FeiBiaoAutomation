import json
from tool.driverTool import driver

# 填写webdriver的保存目录
driver = driver()

# 记得写完整的url 包括http和https
driver.get('http://cpquery.cnipa.gov.cn/')

# 程序打开网页后 “手动登陆账户”
input()

with open('cookies.txt', 'w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))

driver.close()
