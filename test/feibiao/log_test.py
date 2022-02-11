import json

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'cookies': '__yjs_duid=1_f50ea5d576c21c72a76037da730b3b6c1644547888095; JSESSIONID=8A61A0D8A6E43C588ADFD139C9BD2A68'
}

param = {
    'page': 1,
    'limit': 10
}

log_url = 'http://www.ipfeibiao.com/manager/sysLog/list'

response = requests.post(url=log_url, params=param, headers=headers)
list_data = response.json()

fp = open('./log.json', 'w', encoding='utf-8')
json.dump(list_data, fp=fp, ensure_ascii=False)