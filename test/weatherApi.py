import requests
from pprint import pprint
from geopy.geocoders import Nominatim

# ? Open Weather Map
# ! Tốc độ rất nhanh, icon đẹp
# * Free: Current weather, forecast 7days/daily, Gov alerts, weather map, historical 5days
# * Tìm = city, code, geographical coordinates

nameCity = "Hau Giang"
geolocator = Nominatim(user_agent="Virtual Assistant")
location = geolocator.geocode(nameCity)

api = "4e7ced343986de64b7f54296a111c208"
lat = location.latitude
lon = location.longitude
lang = "vi"
part = "hourly,minutely,daily"
url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}&units={}&lang={}"
url_onecall = url.format(lat, lon, part, api, "metric", lang)

print(location.address)
result = requests.get(url_onecall).json()["current"]["weather"]
pprint(result)


""" 
# ? WeatherBit.io
# ! tốc độ khá chậm, icon đẹp
# * Free: current weather, historical, forecast 14days

city = "can tho"
apiKey = "2bc51106f570442ca72aef366b919c5e"
units = "m"

# current weather
url_currentWeather = "https://api.weatherbit.io/v2.0/current?city={}&key={}&units{}".format(
    city, apiKey, units)

url_forecast = "https://api.weatherbit.io/v2.0/forecast/daily?city={}&key={}&units{}".format(
    city, apiKey, units)

# response = requests.get(url_currentWeather)
# pprint(response.json())
 """


""" 
# ? Weather Stack
# * khá nhanh, icon xấu, 
# ! free chỉ có current weather
params = {
    'access_key': '12495524d1b0334e5e77db3787c6d2e3',
    'query': 'Can Tho',
    'units': 'm',
}

api_result = requests.get('http://api.weatherstack.com/current', params)
api_response = api_result.json()
pprint(api_response)

 """
