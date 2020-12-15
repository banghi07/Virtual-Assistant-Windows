import requests
import datetime

url = "https://ipinfo.io/"
response = requests.get(url).json()
city = response["city"]
region = response["region"]
location = response["loc"].split(",")

api = "BL83E6LF3XI3"
url = "http://api.timezonedb.com/v2.1/get-time-zone?key={}&format=json&by=position&lat={}&lng={}".format(
    api, location[0], location[1]
)

response = requests.get(url).json()

u = int(response["gmtOffset"]) / 3600

if u >= 0:
    utc = "+" + "{:.0f}".format(u)
else:
    utc = str("{:.0f}".format(u))

# t = datetime.datetime.now()

# year = t.strftime("%Y")
# month = t.strftime("%m")
# day = t.strftime("%d")
# hour = t.strftime("%H")
# minute = t.strftime("%M")

t = response["formatted"]

year = t[0:4]
month = t[5:7]
day = t[8:10]
hour = t[11:13]
minute = t[14:16]
second = t[17:19]

result = {
    "zone_name": response["zoneName"],
    "utc": utc,
    "year": year,
    "month": month,
    "day": day,
    "hour": hour,
    "minute": minute,
    "second": second,
}
print(result)
# print(response)
