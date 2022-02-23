from tool.patent_query_tool import login_patent_inquiry_gettoken, get_cookies

token = login_patent_inquiry_gettoken(2017107806169)
print(token)
cookies = get_cookies()
print(cookies)