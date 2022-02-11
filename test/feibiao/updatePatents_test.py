import json

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
    'Cookie': '__yjs_duid=1_f50ea5d576c21c72a76037da730b3b6c1644547888095; JSESSIONID=8A61A0D8A6E43C588ADFD139C9BD2A68'
}

param = {
    'token': '23D20FA47ED444ACAC5D8C3F54BA09E1',
    'host': '49.7.96.252',
    'port': '16819',
    'cookie': 'UR3ZMlLdcLIE80S=5.7fmxR0Qd8SKwLmfru7g93cQJJ5I.u7J7.w.8kfrJSdIXDwS3Nh.mDl3SNM6da4; _gscu_930750436=44547890yj2esn10; _gscbrs_930750436=1; bg6=71|BCJpS; JSESSIONID=7b53839cd9fc5772fb725225285d; _gscs_930750436=t445649212kjvfm79|pv:1; UR3ZMlLdcLIE80T=4G8UzwZGRH6NcZjzgj3fJqZU8_9JRB8YioUmshfRxWBo.6EmR1HXLcSDbuOZo9yVYGpPZlPPHJotR5ukqiNrOT3XPSoZO50T3YZXepKyLAj4oRMgHksvRm.ke6N7xNRGx_I0Ia57bovZ9IhDTcleM6ewPO.ZZ1BgY7jz7cI6IH0UE8XB4kt_W4PLLGxV1PZ3xUEnX5WGt7Klhu1DAG5I4q4q1UWFvktvwgKZidxG_E16BK2qDqHSB7.C5KA26fsTATPNn8sBNDfA2PejrH74Oao_fI57zTtiYg_Watx0q7aDZHGgjypR8Vw_aSUgJLc5kmLQ67PfNI2IFwrc8CVn9bzFr',
    'app_no_like': '',
    's_state': ''
}

updatePatents_url = 'http://www.ipfeibiao.com/manager/patentUpdateAnnualState/updatePatents'

response = requests.post(url=updatePatents_url, params=param, headers=headers)
list_data = response.json()

fp = open('./updatePatents.json', 'w', encoding='utf-8')
json.dump(list_data, fp=fp, ensure_ascii=False)