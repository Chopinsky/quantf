from data import import_data
from train import train
import pandas as pd


def run():
    v_df = import_data()

    real_front = [34.575, 39.075, 41.775, 39.625, 39.725]
    real_back = [33.075, 36.225, 38.675, 37.375, 37.725]

    real = pd.DataFrame(data={'front': real_front, 'back': real_back})
    result = train(v_df, real)

    print(result)


if __name__ == "__main__":
    run()

