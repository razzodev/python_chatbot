from math import sin, cos, sqrt, atan2, radians
from my_location import geo_data, user_latitude, user_longitude
from geopy.geocoders import Nominatim


def calc_distance(msg):
    geolocator = Nominatim(user_agent="chatbot")
    location = geolocator.geocode(msg)
    R = 6373.0

    lat1 = radians(float(user_latitude))
    lon1 = radians(float(user_longitude))
    lat2 = radians(location.latitude)
    lon2 = radians(location.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance)
