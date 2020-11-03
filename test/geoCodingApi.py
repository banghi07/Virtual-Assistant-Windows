import requests
from pprint import pprint

# ! API không dùng được => phải trả phí
api = "AIzaSyBNPasppAcUvEuuSB97iCTlxxzMew1y6Xc"
city = "Can Tho"

url_geoCoding = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
    city, api)

result = requests.get(url_geoCoding)
pprint(result.json())
