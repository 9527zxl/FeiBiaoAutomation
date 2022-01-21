from tool.driverTool import driver

driver = driver()
driver.get('http://cpquery.cnipa.gov.cn/')

all_ = driver.window_handles
print(all_)

dq = driver.current_window_handle
print(dq)

