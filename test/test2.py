import random
from time import sleep

from selenium.common.exceptions import TimeoutException

from tool.feibaio_tool import feibiao_login, feibiao_cookie
from tool.patent_query_tool import login_patent_inquiry_gettoken, get_cookies
from tool.patent_update import patent_update, get_patent_number

# # 登录飞镖网
# feibiao_login(username='zhuxingli', password='zhuxingli')
state = True
while state:
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)
    print(patent_number)
    # 获取token
    token = login_patent_inquiry_gettoken(patent_number)
    # 获取cookies
    cookies = get_cookies()
    # 更新年费状态
    patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)
    print(token)
    print('等待中')
    sleep(360)
