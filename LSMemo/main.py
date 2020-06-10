import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


FILE_NAME = "CRM.csv"


def run(debug = False):
    training_set = load(FILE_NAME, debug)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_set = scaler.fit_transform(training_set)

    if debug:
        print(scaled_set)


def load(file, debug = False):
    if file is None:
        return None

    train = pd.read_csv(file)
    training_set = train.iloc[:, 1:2].values

    if debug:
        print(train.head())
        print()

    return training_set


if __name__ == '__main__':
    run(True)
    print("Done!")
