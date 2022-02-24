import random

from tool.feibaio_tool import feibiao_login, feibiao_cookie
from tool.patent_query_tool import login_patent_inquiry_gettoken, get_cookies
from tool.patent_update import patent_update, get_patent_number

# 获取飞镖网cookies
feibiao_cookie = feibiao_cookie()

patent_gather = get_patent_number(feibiao_cookie)
patent_number = random.choice(patent_gather)
print(patent_number)

token = login_patent_inquiry_gettoken(patent_number)
print(token)

cookies = get_cookies()
print(cookies)

patent_update(feibiao_cookie=feibiao_cookie, update_token=token, update_cookie=cookies)

# # 登录飞镖网
# feibiao_login(username='zhuxingli', password='zhuxingli')
