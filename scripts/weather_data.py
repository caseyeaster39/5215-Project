import requests
import time


def weather_req_now(latlong):
    lat = latlong[0]
    lon = latlong[1]

    start = time.time()
    cnt = 1
    key = '5a37683754d15ce2739e21efd5f84146'

    request_url = 'http://history.openweathermap.org/data/2.5/history/city?'

    payload = {
        'lat': lat,
        'lon': lon,
        'start': start,
        'cnt': cnt,
        'key': key
    }

    resp = requests.get(request_url, params=payload)
    resp.raise_for_status()

    return resp.json()


def process_weather_response(resp):
    # Format response data as needed
    pass


# For testing
lat_long = (33, -97)
print(weather_req_now(lat_long))
