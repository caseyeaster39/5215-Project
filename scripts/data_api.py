import weather_data as wd
import zip_code_utils as zcu

from datetime import datetime


def find_additional_info(lat, lon, input_date=None):
    out_dict = {}
    if not input_date:
        input_date = datetime.now()

    latlong = (lat, lon)

    zipcode = int(zcu.find_zip([latlong])[0])
    population_info = zcu.search_by_zip(zipcode).to_dict()
    weather_info = wd.search_weather(lat, lon, input_date)

    hour_search = (input_date.hour - 3)
    if (input_date.hour - 3) < 0:
        hour_search = 0
    elif (input_date.hour - 3) > 23:
        hour_search = 23
    hour_row = weather_info.iloc[hour_search, :].to_dict()

    for key in population_info.keys():
        val = population_info[key]
        if isinstance(val, list):
            for list_index, list_val in enumerate(val):
                if list_index == 0:
                    out_dict[key] = list_val
                else:
                    list_key = key + str(list_index)
                    out_dict[list_key] = list_val
        else:
            out_dict[key] = val

    for item in hour_row.keys():
        out_dict[item] = hour_row[item]

    return out_dict
