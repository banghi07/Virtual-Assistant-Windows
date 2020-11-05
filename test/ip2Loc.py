import requests
from pprint import pprint

getIP = requests.get("https://api.myip.com").json()

# url = "http://api.ipstack.com/{}?access_key=ff657782fd652fd5adf54ed914e91387".format(
#     getIP["ip"])
# result = requests.get(url).json()

# pprint(result)

# .format(getIP["ip"])
url = "https://ipinfo.io/{}/region?token=0b031e6458a2a9".format(getIP["ip"])
result = requests.get(url)

name = result.text
# print(getIP["ip"])
print(name.rstrip("\n"))
print("a")
