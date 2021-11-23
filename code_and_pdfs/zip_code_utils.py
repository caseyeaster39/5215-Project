import requests

import numpy as np
import pandas as pd

from requests.auth import HTTPBasicAuth
from uszipcode import SearchEngine


def find_zip(latlong_list):                                                 # Takes a list of tuples, form [(lat, long)]
    try:
        df = pd.read_hdf('.data_cache/US_long_lat_to_zip.h5', 'df')         # Try reading hdf5 lat longs for USA
    except FileNotFoundError:
        df = pd.read_csv('../ref/US_long_lat_to_zip.csv', dtype=str)        # Read from CSV
        df.to_hdf('./.data_cache/US_long_lat_to_zip.h5', 'df')              # Store as hdf5 for future
        print('caching...')
    best_zips = []
    for coord in latlong_list:                                              # Loop through input list
        lat = coord[0]
        lon = coord[1]
        best_zip = None
        best_zip_distance = None
        for index, row in df.iterrows():                                    # Loop through USA latlongs
            x1 = float(row['LAT'])
            y1 = float(row['LNG'])
            x_dif = (lat - x1)**2
            y_diff = (lon - y1)**2
            distance = np.sqrt(x_dif + y_diff)
            if not best_zip_distance or distance < best_zip_distance:
                best_zip_distance = distance
                best_zip = row['ZIP']
        best_zips.append(best_zip)
    best_zips = list(set(best_zips))
    return best_zips


def get_population(lat, lon):
    request_url = "https://service.zipapi.us/population/zipcode/{zip}/" \
                  "?X-API-KEY={key}&fields=male_population,female_population"
    zip_ = list((lat, lon))
    local_zip = find_zip(zip_)
    key = '426151a147801b8aa34933bbd2c75abc'
    submit_url = request_url.format(zip=local_zip, key=key)
    usr = 'zacharyobrien2@my.unt.edu'
    pas = 'ft2x8A!XmuY@XA6hk9xD*nsw'
    r = requests.get(submit_url, auth=HTTPBasicAuth(usr, pas))
    return local_zip, r.json()['data']['population']


def search_by_zip(zip_):
    search = SearchEngine(simple_zipcode=True)  # set simple_zipcode=False to use rich info database
    zipcode = search.by_zipcode(zip_)
    return zipcode


def zips_unique_create():
    try:
        latlong_df = pd.read_hdf('.data_cache/data_latlong_table.h5', 'df')
    except FileNotFoundError:
        traffic_df = pd.read_csv('../../bigquery-geotab-intersection-congestion/train.csv')
        latlong_df = traffic_df[['IntersectionId', 'Latitude', 'Longitude']].drop_duplicates('IntersectionId')
        latlong_df.to_hdf('./.data_cache/data_latlong_table.h5', 'df')
        print('caching...')

    latlong_list = []
    for _, row in latlong_df.iterrows():
        latlong_list.append((row['Latitude'], row['Longitude']))

    zips = pd.Series(find_zip(latlong_list))
    zips.to_hdf('./.data_cache/dataset_zips.h5', 'df')
    print('caching...')
    return zips


def load_dataset_zips():
    try:
        zips = pd.read_hdf('.data_cache/dataset_zips.h5', 'df')
    except FileNotFoundError:
        zips = zips_unique_create()
    return zips
