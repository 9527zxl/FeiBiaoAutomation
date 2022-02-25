import json

import requests

from tool.feibaio_tool import getdriver, feibiao_cookie
from tool.patent_update import update_successfully

if __name__ == '__main__':
    # 获取飞镖网cookies
    feibiaCookie = feibiao_cookie()
    update_successfully(feibiaCookie)