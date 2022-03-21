import asyncio
import random
import threading
from time import sleep

from tool.feibaio_tool import feibiao_login, feibiao_cookie, getdriver
from tool.patent_query_tool import get_cookies, gettoken, login
from tool.patent_update import patent_update, update_successfully, get_acquisition_patent_Number, get_patent_number, \
    annual_fee_to_update


def main():
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    driver = getdriver()
    login(driver)

    def flow_path():
        # 获取专利号
        patent_gather = get_patent_number(feibiaCookie)
        patent_number = random.choice(patent_gather)
        print('专利号:' + str(patent_number))
        # 获取token
        token = gettoken(patent_number, driver)
        print('token:' + token)
        # 获取cookies
        cookies = get_cookies()
        print('cookies:' + cookies)
        patent_update(feibiao_cookie=feibiaCookie, update_token=token, update_cookie=cookies)

    count = 0
    s1 = update_successfully(feibiaCookie)

    flow_path()
    print('第1次更新完成')
    while True:
        sleep(30)
        s2 = update_successfully(feibiaCookie)
        print('s1=' + str(s1))
        print('s2=' + str(s2))
        print()

        if s1 < s2:
            s1 = update_successfully(feibiaCookie)
            flow_path()
            count += 2
            print('第' + str(count) + '次更新完成')


def collection_and_update():
    driver = getdriver()
    login(driver)
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    # 获取专利号
    patent_number = random.choice(get_acquisition_patent_Number(feibiaCookie, state=False))
    print(patent_number)
    # 获取token
    token = gettoken(patent_number, driver)
    print(token)
    # 获取cookies
    cookies = get_cookies()
    print(cookies)
    # 获取id
    ids = get_acquisition_patent_Number(feibiaCookie, state=True)
    print(ids)
    for id in ids:
        annual_fee_to_update(feibiao_cookie=feibiaCookie, update_cookie=cookies, update_token=token, id=id)


def get_token_and_cookies():
    driver = getdriver()
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    patent_number = random.choice(get_acquisition_patent_Number(feibiaCookie, state=False))
    # 获取token
    token = gettoken(patent_number, driver)
    print(token)
    driver.quit()
    # 获取cookies
    cookies = get_cookies()
    print(cookies)


# main()
# driver = getdriver()
# login(driver)
collection_and_update()
# # 登录飞镖网
# feibiao_login(username='zhuxingli', password='zhuxingli')
# get_token_and_cookies()
