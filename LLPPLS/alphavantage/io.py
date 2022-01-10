from typing import Union
from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd


DATETIME_FORMAT = '%Y-%m-%d'


def read(key: str, sym: str, require_updates: bool = False, crypto: bool = False) -> Union[pd.DataFrame, None]:
	file = Path('../data/' + sym + '.csv')
	downloaded = False

	if require_updates or not file.is_file():
		if not download_file(key, sym, file, crypto=crypto):
			return None

		downloaded = True

	df = pd.read_csv(file, index_col=0, parse_dates=True, na_values=['NaN'])
	df = df.dropna()

	today = datetime.today()
	if not downloaded \
		and today.strftime(DATETIME_FORMAT) != df.index[-1].strftime(DATETIME_FORMAT) \
		and (df.index[-1].isoweekday() != 5 or today - df.index[-1] > timedelta(4)):
		if not download_file(key, sym, file, df.index[-1] + timedelta(1), crypto=crypto):
			return None

		df = pd.read_csv(file, index_col=0, parse_dates=True, na_values=['NaN'])
		df = df.dropna()

	df = df[['adjOpen', 'adjHigh', 'adjLow', 'adjClose', 'adjVolume']]
	df.columns = ['open', 'high', 'low', 'close', 'volume']

	df['pct'] = df['close'].pct_change(periods=5) * 100
	df['ewma'] = df['close'].ewm(span=8).mean()
	df['zscore'] = (df['close'] - df['close'].rolling(21).mean()) / df['close'].rolling(21).std()

	# pct average
	vals = df['close'].pct_change()
	multi = 1 + vals

	for i in range(1, 5):
		multi *= 1 + vals.shift(i)

	df['pct_avg'] = pow(multi, -5) - 1

	# print(df['zscore'])
	# print(df['pct_avg'])

	return df


def download_file(key: str, sym: str, file: Path, start_date=None, crypto: bool = False) -> bool:
	if not key:
		return False

	if not crypto:
		base = 'https://api.tiingo.com/tiingo/daily/' + sym + '/prices'
	else:
		base = 'https://api.tiingo.com/tiingo/crypto/prices'

	end_date = datetime.today()
	mode = 'a'

	if not start_date:
		start_date = end_date - timedelta(10*365)
		mode = 'w'

	base += '?token=' + key

	if crypto:
		base += '&tickers=' + sym + '&resampleFreq=1day'

	base += '&startDate=' + start_date.strftime(DATETIME_FORMAT) + '&endDate=' + end_date.strftime(DATETIME_FORMAT)
	base += '&format=csv'

	response = requests.get(base)
	print("Write mode:", sym, mode)

	with open(file, mode) as csv_file:
		if mode == 'a':
			csv_file.write('\n'.join(response.text.split('\n')[1:]))
		else:
			csv_file.write(response.text)

		csv_file.close()

	print('Data saved for ' + sym + '; from: ' + base)

	return True
