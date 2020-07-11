from matplotlib import pyplot as plt
# from matplotlib import interactive
import numpy as np
import pandas as pd
from lppls import lppls
from crawler import crawl


def read_data(ticket, data_only=False):
    src = "data/" + ticket + ".csv"
    data = pd.read_csv(src, index_col="Date")

    # remove empty cells
    data = data[data["Adj Close"].notnull()]
    print("data shape:", data.shape)

    if data_only:
        return data

    t_len = len(data)

    date = data.index
    time = np.linspace(0, t_len - 1, t_len)
    close = [data["Adj Close"][i] for i in range(len(data["Adj Close"]))]

    return [time, close, date]


# revised version of the LPPL without φ
def lppl(t, tc, m, w, a, b, c1, c2):
    return a + np.power(tc - t, m) * (b + ((c1 * np.cos(w * np.log(tc - t))) + (c2 * np.sin(w * np.log(tc - t)))))


def calc(ticket, count=25):
    data = read_data(ticket, data_only=True)

    # convert index col to evenly spaced numbers over a specified interval
    time = np.linspace(0, len(data) - 1, len(data))

    # create list of observation data, in this case,
    # daily adjusted close prices of the S&P 500
    price = [p for p in data["Adj Close"]]

    # create Mx2 matrix (expected format for LPPLS observations)
    observations = np.array([time, price])

    # set the max number for searches to perform before giving-up
    # the literature suggests 25
    max_searches = count

    # instantiate a new LPPLS model with the S&P 500 data set
    lppls_model = lppls.LPPLS(use_ln=True, observations=observations)

    # fit the model to the data and get back the params
    print("ready to fit ... ", count)
    tc, m, w, a, b, c = lppls_model.fit(observations, max_searches, minimizer='Nelder-Mead')

    # visualize the fit
    predict = lppls_model.plot_fit(observations, tc, m, w)

    print("done with ... ", count)

    return predict


def run(ticket="spx"):
    crawl(ticket)
    print("data updated ...")

    # data2 = calc(ticket, count=5)
    data1 = calc(ticket, count=25)

    t = data1['Time'].tolist()
    obs = data1['Observations'].tolist()
    fit1 = data1['LPPLS Fit'].tolist()
    # fit2 = data2['LPPLS Fit'].tolist()

    plt.plot(t, fit1, label="long")
    # plt.plot(t, fit2, label="short")
    plt.plot(t, obs, label="price")
    plt.legend(loc="upper left")

    plt.savefig("./history/" + ticket + ".png")
    plt.show()

    print("all done ...")


run("lulu")
