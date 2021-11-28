import os

import pandas as pd

from joblib import load
from datetime import datetime
from data_api import find_additional_info


def get_input():
    while True:
        lat, long = input("Enter coordinates (e.g: 33.205317, -97.153130): ").split(',')
        lat, long = float(lat), float(long)
        if isinstance(lat, (float, int)) and isinstance(long, (float, int)):
            break
        else:
            print("Invalid coordinate pair, please reenter.")

    day = None

    check = input("Would you like to use the current time? (y/n): ")
    if check.lower() == 'n':
        while True:
            day = input("Please enter date (DD/MM/YYYY): ")
            try:
                day = datetime.strptime(day, '%d/%m/%Y')
                break
            except ValueError:
                print("Invalid input, please try again.")
    return lat, long, day


def input_process():
    input_data = get_input()
    data_dict = find_additional_info(*input_data)
    df = pd.DataFrame(data_dict, index=[0])

    features = ["Hour", "Weekend", "Month", "radius_in_miles", "population",
                "population_density", "land_area_in_sqmi", "water_area_in_sqmi",
                "housing_units", "occupied_housing_units", "median_home_value",
                "median_household_income", "temp", "dwpt", "rhum", "prcp",
                "wdir", "wspd", "pres", "coco"]
    return df[features]


def load_models():
    models = {}
    for root, dirs, files in os.walk("../notebooks/model_cache", topdown=False):
        for name in files:
            model_path = os.path.join(root, name)
            print(f"Loading: {model_path}")
            models[name.split('.')[0]] = load(model_path)
            print("Done.")
    return models


def make_inference(model, input_data):
    percentiles = ['P20', 'P40', 'P50', 'P60', 'P80']
    print('\n############################')
    print(f'Predicting with {str(model["regr"])}:')
    print('Wait expected')
    preds = model["model"].predict(input_data)[0]
    for i in range(len(preds)):
        print(f'\t{percentiles[i]}: {round(preds[i])} s.')
    print('############################\n')


def main():
    input_data = input_process()
    model_dict = load_models()
    for model in model_dict:
        make_inference(model_dict[model], input_data)


if __name__ == '__main__':
    main()
