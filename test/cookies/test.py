import json

with open('cookeis.json', 'r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)

    # for id in cookies_list:
        # print(id['name'])

    print(cookies_list[1]['name'])
    # cookie = ''
    # for id in cookies_list:
    #     text = id['name'] + '=' + id['value'] + ';'
    #     cookie += text
    #     cookie += "\n"
    #     # cookie.join(text)
    #     # print(text)
    # print(cookie)
