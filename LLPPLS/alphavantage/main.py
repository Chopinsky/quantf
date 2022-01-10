import datetime
import getopt
import os
import sys

import pandas
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from alphavantage.io import read
from alphavantage.process import localMaxMin


load_dotenv()

API_KEY = os.getenv('TIINGO_KEY')
SYMBOLS = ['spxl', 'tqqq', 'urty', 'bcx', 'soxl', 'vnq', 'tlt', 'gld']
START_DATE = datetime.datetime(2012, 1, 1)
END_DATE = datetime.datetime.now()
RELOAD = False
HIGH_LOW_PLOT = True


def run_sym(symbol: str):
	fig, ax = None, None

	if not HIGH_LOW_PLOT:
		fig, ax = plt.subplots(1, 1, figsize=(10, 7))

	df = read(API_KEY, symbol, RELOAD)
	df = localMaxMin(df, symbol, n=4, plot=HIGH_LOW_PLOT, ax=ax if ax is not None else None)

	'''
	agg = df['close']
	agg_pct = df['pct']
	agg_ema = df['ewma']
	'''

	if fig and ax:
		for ax in fig.axes:
			plt.sca(ax)
			plt.xticks(rotation=30)

		fig.tight_layout()
		plt.show()


def run_preset():
	init = False
	agg, agg_pct, agg_ema = None, None, None
	fig, ax = None, None

	if not HIGH_LOW_PLOT:
		fig, ax = plt.subplots(3, 3, figsize=(14, 7))

	for i, symbol in enumerate(SYMBOLS):
		x, y = i // 3, i % 3
		df = read(API_KEY, symbol, RELOAD)
		df = localMaxMin(df, symbol, n=4, plot=HIGH_LOW_PLOT, ax=ax[x, y] if ax is not None else None)

		if not init:
			agg = pandas.DataFrame(columns=SYMBOLS, index=df.index)
			agg_pct = pandas.DataFrame(columns=SYMBOLS, index=df.index)
			agg_ema = pandas.DataFrame(columns=SYMBOLS, index=df.index)
			init = True

		agg[symbol] = df['close']
		agg_pct[symbol] = df['pct']
		agg_ema[symbol] = df['ewma']

	if fig:
		for ax in fig.axes:
			plt.sca(ax)
			plt.xticks(rotation=30)

		fig.tight_layout()
		plt.show()


if __name__ == '__main__':
	argv = sys.argv[1:]

	try:
		opts, args = getopt.getopt(argv, "s:")
	except getopt.GetoptError:
		print('main.py -s <symbols, divided by comma>')
		sys.exit(2)

	sym = None
	for opt, arg in opts:
		if opt == '-s':
			sym = arg.split(',')

	if not sym:
		run_preset()
	else:
		run_sym(sym)
