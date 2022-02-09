from lxml import etree

import requests

Cookie = 'UR3ZMlLdcLIE80S=yMZsawJJmfQ9i8IUWKWmai9UYx5KsHN0yORMOO_r3lBwstcyi6J8s6SKc3fr0Ik6; _gscu_930750436=44288851hwvoiz18; UR3ZMlLdcLIE80T=4A177qtpi3KrBbcRnCpjTc2PwKLDyPFw8qsbXqZTj11xoGjhM1RuPc8t1_slGvJjXBPchi188_zysHjcK4MGBcerS.10yFePg287aebttJ2ToXC8nN.K_BsDJZ07wbUWDjozVnE3.JahM2OmCFpM0O0Artvl5cgkId4EfTJZJ5vs0SbNxeR7OkKsY.HCxNjUzyKEs2ZGwh0EobD91IcOOj5CKeWz55BunsCVBmHyfygvY4qK8KsZznVz4e0tAnATAiMoSF5VetzI9MTqumfS1Han8QlSZ5W.cINnhHu.7_m57mTCMVBfFs0aLC66iG4CNLQjQbKMhBhaUkZDhJosIRA5LPdvdx2p5_GUdhsUqciqdaZrz5RIfRVq6D6a.NYVHEOA; UR3ZMlLdcLIE83S=Hqx.K.cT3vdgiKu0YOqLKGoRo99fdQxhbSf7TCoE195YbzDu02wIxd49O1ERDyhQ; bg6=66|BB+oY; JSESSIONID=cf3b66f67c6e4fff4da3b68a8260; _gscbrs_930750436=1; _gscs_930750436=44384467s431r118|pv:1; UR3ZMlLdcLIE83T=47qzio1Y7GlA15.eK5Jhe1hqN2l5XWYKn37QWETKjZr20DhW2fZh65O4MKqmbHu2R5BvrwnivDo0LPBKgkeDkBw_5oE5spGqscTu11RiQ24ylPexIo6Pw1786KqPJcsMWEZkljNR7uz65e7HKDy5zrk_geEZ3y_nVZ03k15vAp1nmP0v9rLPKRg_d5FY4k4Hk7ICyQ_pPW91yEVu0s6hinmDQKkpVNaxnIrFirQ3tt3wsAh_EL8CFZX0JvSPPTw3I4ogI3SqouGWX1p.WNUB4AaSOHRvMmoEF0roMeKEcwT9m3xS59BQJxh2eHkviOsjw_TGA30e3sP6VVZITxEv3QOi67FIt5CcnIfQfixE_xv7_d4bIZsVLpMaMH66uLCixnc3'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0',
    'Cookie': Cookie  # 登录成功后，将cookie放这里
}

member_url = 'http://cpquery.cnipa.gov.cn/txnQueryBibliographicData.do?select-key:shenqingh=2019201307053'
response = requests.get(member_url, headers=headers)
data = response.content.decode('utf-8')
print(data)

print(response.cookies)

code_url = 'http://cpquery.cnipa.gov.cn/freeze.main?txn-code=createImgServlet'

url = 'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=2017107806169&verycode=10'
