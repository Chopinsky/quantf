from zipline.api import order_target, record, symbol


def initialize(context):
    context.i = 0
    context.asset = symbol('AAPL')


def handle_data(context, data):
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 40:
        return

    # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_sma = data.history(context.asset, 'price', bar_count=20, frequency="1d").mean()
    long_sma = data.history(context.asset, 'price', bar_count=40, frequency="1d").mean()

    # Trading logic
    if short_sma > long_sma:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target(context.asset, 100)
    elif short_sma < long_sma:
        order_target(context.asset, 0)

    # Save values for later inspection
    record(AAPL=data.current(context.asset, 'price'),
           short_mavg=short_sma,
           long_mavg=long_sma)
