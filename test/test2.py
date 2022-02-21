import json

cookie = ''
with open('../temporary/cookies.json', 'r') as f:
    cookies_list = json.load(f)
    for cookies in cookies_list:
        cookie += cookies['name'] + '=' + cookies['value'] + ';'
print(cookie)