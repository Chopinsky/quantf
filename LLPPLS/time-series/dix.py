import csv
from matplotlib import pyplot as plt


def read(loc):
    df = []

    with open(loc, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'{row["Date"]} -- {row["Adj Close"]} / {row["Volume"]}')
                df.append(row)
                line_count += 1

        # print(f'Processed {line_count-1} lines.')

    return df


def find_turns(data, col="Adj Close", to_print=True):
    size = len(data)
    peaks = [data[i] for i in range(1, size-1) if data[i][col] > data[i-1][col] and data[i][col] > data[i+1][col]]
    dips = [data[i] for i in range(1, size-1) if data[i][col] < data[i-1][col] and data[i][col] < data[i+1][col]]

    peak_time, peak_close = [], []
    dip_time, dip_close = [], []

    for p in peaks:
        peak_time.append(p['Date'])
        peak_close.append(float(p['Adj Close']))

    for p in dips:
        dip_time.append(p['Date'])
        dip_close.append(float(p['Adj Close']))

    if to_print:
        plt.figure()

        plt.subplot(211)
        plt.plot(peak_time, peak_close, "ro")

        plt.subplot(212)
        plt.plot(dip_time, dip_close, "ro")

        plt.show()

    return peak_time, peak_close, dip_time, dip_close


src = read("../data/spy.csv")
find_turns(src)
