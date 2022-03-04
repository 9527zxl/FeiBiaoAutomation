import random
from time import sleep

from selenium.common.exceptions import TimeoutException

from tool.feibaio_tool import feibiao_login, feibiao_cookie
from tool.patent_query_tool import get_cookies, gettoken
from tool.patent_update import patent_update, get_patent_number, update_successfully


# # 登录飞镖网
# feibiao_login(username='zhuxingli', password='zhuxingli')

def main():
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)
    # 获取token
    token = gettoken(patent_number)
    # 获取cookies
    cookies = get_cookies()
    patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)
    print('第一次更新完成')

    s1 = update_successfully(feibiaCookie)
    count = 0
    while True:
        sleep(30)
        s2 = update_successfully(feibiaCookie)
        print()
        print('s1=' + str(s1))
        print('s2=' + str(s2))
        print()

        if s1 < s2:
            s1 = update_successfully(feibiaCookie)

            # 获取专利号
            patent_gather = get_patent_number(feibiaCookie)
            patent_number = random.choice(patent_gather)
            # 获取token
            token = gettoken(patent_number)
            # 获取cookies
            cookies = get_cookies()

            print('开始更新')
            print('专利号:' + str(patent_number))
            print('token:' + token)
            print('cookies:' + cookies)
            patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)
            count += 1
            print('第' + str(count) + '次更新完成')


main()
