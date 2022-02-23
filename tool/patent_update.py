import json

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

    response = requests.post(url=patent_update_url, params=param, headers=headers)
    list_data = response.json()

    fp = open('./updatePatents.json', 'w', encoding='utf-8')
    json.dump(list_data, fp=fp, ensure_ascii=False)
