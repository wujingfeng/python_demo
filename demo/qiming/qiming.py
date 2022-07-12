import json

import execjs
import requests

url = "https://vipapi.qimingpian.cn/Search/searchVip"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "vipapi.qimingpian.cn",
    "Origin": "https://www.qimingpian.cn",

}
data = {
    'keywords': '浙江新码生物医药有限公司',
    'type': '1',
    'page': '1',
    'num': '20',
    'unionid': 'bZiWlSsCI5ZFi+3QDsgRgRfU9HdLI1Bl4+bB6GFWpLjqRpwVLPYDOYGqklhQlfUXeJWqqIs6kiQsM8IbOYgM5A=='
}

response = requests.post(url=url, headers=header, data=data)
text = response.text
text = json.loads(text)
encrypt_data = text['encrypt_data']
print(text)

with open('123.js', 'r', encoding='utf-8') as f:
    reader = f.read()

loader = execjs.compile(reader)

res = loader.call("s", encrypt_data)
print(res)
