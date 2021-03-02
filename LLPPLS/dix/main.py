import pandas as pd
import matplotlib.pyplot as plt
import dateutil.parser as parser


def read(loc='dix.csv'):
    df = pd.read_csv(loc, index_col="date")

    df['dix_rank'] = df['dix'].rank(method='max', pct=True)
    df['gex_rank'] = df['gex'].rank(method='max', pct=True)

    print(df)
    return df


if __name__ == "__main__":
    data = read()

    data[['dix_rank', 'gex_rank']][data.index > "2020-11-04"].plot()
    plt.show()

    print('done ... ')
