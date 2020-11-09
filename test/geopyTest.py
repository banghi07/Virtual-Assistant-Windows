from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Virtual Assistant")
location = geolocator.geocode("can tho")
print(location.latitude, location.longitude)
print(location.address)
# print(location.raw)
