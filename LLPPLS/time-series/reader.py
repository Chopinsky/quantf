import tensorflow as tf
import pandas as pd
import os
import datetime


def fromURL(origin, name):
    zip_path = tf.keras.utils.get_file(
        # origin='https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip',
        # fname='jena_climate_2009_2016.csv.zip',
        origin=origin,
        fname=name,
        extract=True
    )

    csv_path, _ = os.path.splitext(zip_path)

    df = pd.read_csv(csv_path)
    date_time = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')
    timestamp_s = date_time.map(datetime.datetime.timestamp)

    return df, date_time, timestamp_s


def split(df):
    n = len(df)

    # split data
    train_df = df[0:int(n * 0.7)]
    val_df = df[int(n * 0.7):int(n * 0.9)]
    test_df = df[int(n * 0.9):]

    # standardize data
    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    # the num of features is the same as the length
    num_features = df.shape[1]

    return train_df, val_df, test_df, num_features
