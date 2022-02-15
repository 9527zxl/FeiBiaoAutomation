from tool.tool import getdriver

if __name__ == '__main__':
    driver = getdriver()
    driver.get('http://cpquery.cnipa.gov.cn/')
