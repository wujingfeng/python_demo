import requests


'''
飞卢小说网
'''
url = "https://b.faloo.com/550081_60.html"

response = requests.get(url=url)
print(response.text)