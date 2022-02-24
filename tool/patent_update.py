import requests


def patent_update(feibiao_cookie, update_cookie, update_token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'Cookie': feibiao_cookie
    }

    param = {
        'token': update_token,
        'host': '49.7.96.252',
        'port': '16819',
        'cookie': update_cookie,
        'app_no_like': '',
        's_state': ''
    }

    patent_update_url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/updatePatents'

    requests.post(url=patent_update_url, params=param, headers=headers)


# 获取专利号
def get_patent_number(feibiao_cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'cookies': feibiao_cookie
    }

    param = {
        'page': 1,
        'limit': 50
    }

    url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/list'

    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()

    # 年费状态更新数量
    annual_fee_quantity = list_data['count']
    print(annual_fee_quantity)

    patent_gather = []
    for id in list_data['data']:
        patent_gather.append(id['app_no'])

    return patent_gather
