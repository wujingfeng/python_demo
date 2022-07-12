import json

import requests


# 中国石油招标网

def index():


    url = 'https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut'
    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "apifox/1.0.0 (https://www.apifox.cn)",
        "Connection": "keep-alive",
        "Host": "www.cnpcbidding.com",
        "Accept-Encoding": "gzip,deflate,br",
        "Content-Type": "application/json"
    }
    data = {
        "url": "./list.html",
        "pid": "198",
        "pageSize": "15",
        "categoryId": "201",
        "title": "",
        "projectType": "",
        "pageNo": "1",
        "shiXinName": ""
    }

    response = requests.post(url=url, headers=header, data=json.dumps(data))
    data = response.json()
    print(data['list'])
    print(json.dumps(response.json()))
    print(json.loads(json.dumps(response.json())))


index()