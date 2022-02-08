from lxml import etree

import requests

Cookie = 'UR3ZMlLdcLIE80S=O6.6c4SPhM067v.tFFaQoCLWTM9FyT3zsDIg9mgpRqPjAXw2mTP6aFOtSJNwyxyz; _gscu_930750436=305905169oxh6p16; _gscbrs_930750436=1; JSESSIONID=973e6b0e55162abe107e21e46734; bg6=75|BB7ep; UR3ZMlLdcLIE80T=4MahHfKPRbHVymuCEv1KlUbLJa8u9AsyaoEeeLHzz3AteKs7KH8BFKJwykDBSknABDwZFsK4niwbfWfDvtkizkOajKo9gR6H4K37dYFaNMMtLAK6iPJG9NAn8U0eq8befbaTNe5PJfQdEuUr5.emC2bXXiR_7CvhB1Q6rkD4QCo67Mrwws1rSBpScPi.X6RCxPD8bx3gjh4cM9j3E5VfjMZnsHHQ3lp.JSWYxpjwbXMel280JwpKtewvqiBs68tcZfSOtsAZC7Mh_z0GzGQ2kFroR8fQQugIpib5lN6R5Xk3nrxjF4khOaNK0S.tIb0_ZklL9JLK31XcDodxx3tLZdhpiYpf044EOupYzHC9B_CN0pVTUqRzXtLd8HVlZNZpKDTE'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0',
    'Cookie': Cookie  # 登录成功后，将cookie放这里
}

member_url = 'http://cpquery.cnipa.gov.cn/txnQueryBibliographicData.do?select-key:shenqingh=2017107810431'
response = requests.get(member_url, headers=headers)
data = response.content.decode('utf-8')
print(data)

code_url = 'http://cpquery.cnipa.gov.cn/freeze.main?txn-code=createImgServlet'

url = 'http://cpquery.cnipa.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=2017107806169&verycode=10'
