import os.path
import pandas as pd


spot_path = "../data/vix_2012_2017.csv"
front_month_path = "../data/front_month_2020.csv"
back_month_path = "../data/back_month_2020.csv"

front_month_data_path = "https://www.quandl.com/api/v3/datasets/CHRIS/CBOE_VX1.csv"
back_month_data_path = "https://www.quandl.com/api/v3/datasets/CHRIS/CBOE_VX2.csv"


def from_source(remote, local):
    if os.path.isfile(local):
        data = pd.read_csv(
            local,
            index_col="Trade Date",
            usecols=["Trade Date", "Settle"]
        )
    else:
        raw = pd.read_csv(
            remote,
            index_col="Trade Date",
        )

        raw.to_csv(local, index=True)

        # only retain the "Settle" column
        data = raw[["Settle"]]

    data = data.sort_index(axis='index', ascending=True)

    return data


def import_data():
    # get the vix prices
    v_spot = pd.read_csv(
        spot_path,
        index_col="Date",
        usecols=["Date", "Adj Close"]
    )

    # get front month data
    v_front_month = from_source(front_month_data_path, front_month_path)

    # get back month data
    v_back_month = from_source(back_month_data_path, back_month_path)

    # build actual data frame
    v_df = pd.DataFrame(index=v_spot.index, columns=["spot", "front", "back"])

    # copy data to the columns
    v_df["spot"] = v_spot["Adj Close"].shift(-1)
    v_df["front"] = v_front_month["Settle"]
    v_df["back"] = v_back_month["Settle"]

    # drop the last row as it has a NaN from v_spot shifts
    v_df = v_df.drop(v_df.index[len(v_df)-1])

    return v_df

