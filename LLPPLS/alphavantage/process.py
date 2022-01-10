import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema


def localMaxMin(
	src: pd.DataFrame,
	sym: str = '',
	col: str = 'close',
	n: int = 5,
	plot: bool = False,
	plt_col: str = 'zscore',
	ax: any = None
) -> pd.DataFrame:
	"""
	src : data source
	col : the column to find the local max / min with
	n   : the number of points to be checked before and after
	plot : if we shall plot the local max / min
	"""

	# Find local peaks
	min_algo = argrelextrema(src[col].values, np.less_equal, order=n)
	lows = pd.DataFrame(data=src.iloc[min_algo[0]][col], index=src.index)
	src['min'] = lows

	# for (date, row) in zip(lows.index, lows):
	# 	print(date, row)

	max_algo = argrelextrema(src[col].values, np.greater_equal, order=n)
	highs = pd.DataFrame(data=src.iloc[max_algo[0]][col], index=src.index)
	src['max'] = highs

	lows.insert(1, 'marks', [-1] * len(lows))
	lows = lows.dropna()

	highs.insert(1, 'marks', [1] * len(highs))
	highs = highs.dropna()

	combined = pd.concat([lows, highs])
	combined.sort_index(inplace=True)
	# print(combined[-100:])

	# Plot results
	back = -90
	x = src.index[back:]

	if plot:
		y = src[col][back:]
		y0 = src['min'][back:]
		y1 = src['max'][back:]

		# EWMA
		y_ewma = src[col].ewm(span=8).mean()
		# y_pct = src[col].pct_change(periods=5)

		# SMA
		# y_sma = src[col].rolling(8).mean().shift(-3)

		plt.title(sym)
		plt.scatter(x, y0, c='r')
		plt.scatter(x, y1, c='g')
		plt.plot(x, y)
		plt.plot(x, y_ewma[back:])
		plt.show()

	fig_col = 'pct' if plt_col == 'pct' else 'zscore'

	if ax and not plot:
		ax.plot(x, src[fig_col].ewm(span=8).mean()[back:], color='red')
		ax.bar(x, src[fig_col][back:])

		ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
		ax.set_title(sym)

	return src
