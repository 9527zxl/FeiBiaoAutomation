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

url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/list'

response = requests.get(url=url, params=param, headers=headers)
list_data = response.json()

# 年费状态更新数量
annual_fee_quantity = list_data['count']
print(annual_fee_quantity)

patent_gather = []
for id in list_data['data']:
    patent_gather.append(id['app_no'])

print(patent_gather)



# fp = open('./douban.json', 'w', encoding='utf-8')
# json.dump(list_data, fp=fp, ensure_ascii=False)
