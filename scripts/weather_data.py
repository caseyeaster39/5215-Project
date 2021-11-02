import requests


def get_user_key():
    try:
        with open('.key_cache/key.txt', 'r') as fin:
            key = fin.read()
    except FileNotFoundError:
        print('User key not found. You can create an account here: https://home.openweathermap.org/')
        key = input('Please paste your key here: ')
        with open('.key_cache/key.txt', 'w') as fout:
            fout.write(key)
    return key


def weather_req_now(latlong):
    lat = latlong[0]
    lon = latlong[1]
    key = get_user_key()

    request_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}'

    resp = requests.get(request_url)
    resp.raise_for_status()

    return resp.json()


def process_weather_response(resp):
    # Format response data as needed
    pass


# For testing
lat_long = (33, -97)
print(weather_req_now(lat_long))
