import datetime
import itertools
from matplotlib import pyplot as plt
from matplotlib import interactive
import numpy as np
import pandas as pd
import random
from scipy.optimize import minimize
from scipy import linalg
import seaborn as sns


def read_data(src="data/spx.csv"):
    data = pd.read_csv(src, index_col="Date")

    date = data.index
    t_len = len(data)
    time = np.linspace(0, t_len-1, t_len)
    close = [data["Adj Close"][i] for i in range(len(data["Adj Close"]))]
    series = [time, close, date]

    return series


# revised version of the LPPL without φ
def lppl(t, tc, m, w, a, b, c1, c2):
    return a + np.power(tc - t, m) * (b + ((c1 * np.cos(w * np.log(tc - t))) + (c2 * np.sin(w * np.log(tc - t)))))


def run():
    data = read_data()
    size = len(data[0])

    for i in range(size):
        print(data[2][i], data[1][i])

    interactive(True)

    plt.plot(data[0], data[1])
    plt.show()


run()
