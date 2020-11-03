from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Virtual Assistant")
location = geolocator.geocode("hậu giang")
print(location.latitude, location.longitude)
print(location.address)
