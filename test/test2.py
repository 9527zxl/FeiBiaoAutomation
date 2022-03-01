import random
from time import sleep

from selenium.common.exceptions import TimeoutException

from tool.feibaio_tool import feibiao_login, feibiao_cookie
from tool.patent_query_tool import login_patent_inquiry_gettoken, get_cookies
from tool.patent_update import patent_update, get_patent_number, update_successfully


# # 登录飞镖网
# feibiao_login(username='zhuxingli', password='zhuxingli')

def main():
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    s1 = update_successfully(feibiaCookie)
    # 获取专利号
    patent_gather = get_patent_number(feibiaCookie)
    patent_number = random.choice(patent_gather)
    # 获取token
    token = login_patent_inquiry_gettoken(patent_number)
    # 获取cookies
    cookies = get_cookies()
    print('开始更新')
    patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)
    print('第一次更新完成')

    state = True
    count = 0
    while state:
        sleep(30)
        s2 = update_successfully(feibiaCookie)
        print('s1=' + str(s1))
        print('s2=' + str(s2))
        print()

        if int(s1) < int(s2):
            s1 = update_successfully(feibiaCookie)
            # 获取专利号
            patent_gather = get_patent_number(feibiaCookie)
            patent_number = random.choice(patent_gather)
            print('获取专利号:' + patent_number)
            # 获取token
            token = login_patent_inquiry_gettoken(patent_number)
            print('获取token:' + token)
            # 获取cookies
            cookies = get_cookies()
            print('获取cookies:' + cookies)
            # 更新年费状态
            patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)
            count += 1
            print('第' + str(count + 1) + '次更新完成')


def error():
    try:
        main()
        return True
    except Exception:
        return False


while not error():
    main()
