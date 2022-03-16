import json
import random

import requests

from tool.feibaio_tool import getdriver, feibiao_cookie
from tool.patent_query_tool import gettoken, get_cookies
from tool.patent_update import update_successfully, get_acquisition_patent_Number

if __name__ == '__main__':
    driver = getdriver()
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 年费采集专利号
    patent_acquisition = random.choice(get_acquisition_patent_Number(feibiaCookie))
    # 获取token
    token = gettoken(patent_acquisition, driver)
    print('token:' + token)
    # 获取cookies
    cookies = get_cookies()
    print('cookies:' + cookies)
