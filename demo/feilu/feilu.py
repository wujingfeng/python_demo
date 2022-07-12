import requests



url = "https://b.faloo.com/550081_60.html"

response = requests.get(url=url)
print(response.text)