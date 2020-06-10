from zipline.research import prices, symbols
import pandas as pd

symbol = 'NIO'

# Query historical pricing data for AAPL
close = prices(
    assets=symbols(symbol),
    start='2018-06-01',
    end='2020-06-01',
)

# Compute 20 and 50 day moving averages on
# AAPL's pricing data
sma20 = close.rolling(20).mean()
sma50 = close.rolling(50).mean()

# Combine results into a pandas DataFrame and plot
pd.DataFrame({
    symbol: close,
    'SMA20': sma20,
    'SMA50': sma50
}).plot(
    title=symbol + 'Close Price / SMA Crossover'
)
