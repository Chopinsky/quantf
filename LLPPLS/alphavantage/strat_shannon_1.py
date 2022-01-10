import os
from math import floor, exp
from bisect import bisect_left

import pandas
from matplotlib import pyplot as plt
from dotenv import load_dotenv
from alphavantage.io import read

load_dotenv()
API_KEY = os.getenv('TIINGO_KEY')

SYM = 'spy'
RELOAD = False


def rebalance(stock, cash, prev, curr, ratio):
	total = (stock/prev) * curr + cash
	return total * ratio, total * (1 - ratio)


def run_strat(
	df,
	ratio=1.0,
	init=100,
	period=0,
	console=0,
	dynamic_strat=2,
	ratio_jump_response=False,
	price_jump_response=False,
	to_plot=False
):
	last = None
	final = None
	lo_ratio = 0.048
	bound_ratio = lo_ratio
	bounds = [1-bound_ratio, 1+bound_ratio]
	last_ratio = ratio
	stock, cash = init*ratio, init*(1-ratio)

	time = []
	total = []
	stocks = []
	cashes = []
	flow = []
	ratios = []

	dist = [10, 30, 50, 70, 90, 100]
	stack = []
	skip = 0

	for r in df.iterrows():
		curr = r[1]['close']
		if not curr:
			continue

		stack.append(curr)
		if len(stack) > 180:
			stack = stack[-180:]

		if not last:
			last = curr
			final = stock + cash
			continue

		# if wiped out, stop
		curr_stock = stock * curr / last
		if final <= 0 or curr_stock+cash <= 0:
			final, stock, cash = 0, 0, 0
			continue

		ratio_adjusted = ratio
		ratio_changed = False
		big_jump = False

		if dynamic_strat > 0:
			hi, lo = max(stack), min(stack)

			if dynamic_strat == 1:
				# range with linear growth
				pct = int(floor(100*(curr-lo)/(hi-lo)))
				n = bisect_left(dist, pct)
				ratio_adjusted = lo_ratio + (ratio-lo_ratio)*n/5
			elif dynamic_strat == 2:
				# range with log growth
				pct = (curr-lo)/(hi-lo)
				ratio_adjusted = ratio * (1/(1+exp(5-8*pct)) + lo_ratio)
			else:
				# SMA based adjustment
				n = 0
				if curr >= sum(stack[-8:]) / 8:
					n += 1

				if sum(stack[-20:]) / 20:
					n += 1

				if sum(stack[-50:]) / 50:
					n += 1

				if sum(stack[-100:]) / 100:
					n += 1

				if sum(stack[-180:]) / 180:
					n += 1

				ratio_adjusted = lo_ratio + (ratio-lo_ratio)*n/5

			# flash crash, emergency adjustment
			if ratio_adjusted < 1.0 and last_ratio > 1.0:
				# print("emergency rebalance on:", r[0].to_pydatetime().strftime("%x"))
				ratio_changed = True

			if curr/last <= bounds[0] or curr/last >= bounds[1]:
				big_jump = True

		if period > 0:
			if (skip >= period) or (price_jump_response and big_jump) or (ratio_jump_response and ratio_changed):
				skip = 0
			else:
				skip += 1
				continue

		shares = stock/last
		stock, cash = rebalance(stock, cash, last, curr, ratio_adjusted)
		final = stock + cash
		last = curr
		last_ratio = ratio_adjusted
		ratios.append(ratio_adjusted)

		if to_plot:
			time.append(r[0].to_pydatetime())
			total.append(final)
			stocks.append(stock)
			cashes.append(cash)
			flow.append(stock/curr - shares)

		if console & 1 > 0:
			print(r[0].to_pydatetime().strftime("%x"), curr, ratio_adjusted, stock, cash)

	if len(time) > 0:
		# plt.plot(time, flow)
		plt.plot(time, total)
		# plt.plot(time, ratios)
		# plt.plot(time, stocks)
		# plt.plot(time, cashes)

		plt.show()

	if console & 2 > 0:
		r = df.iloc[[-1]]['close']

		print(
			"==============\nsource ratio:", round(ratio, 2), "; rebalance period:", period, "\n=============="
			"\n0. end date:", df.index[-1].to_pydatetime().strftime("%x"),
			"\n1. stock price:", r[0],
			"\n2. leverage:", ratios[-1] if len(ratios) > 0 else "N/A",
			"\n3. stock value:", stock, "( shares:", stock/r[0], ")",
			"\n4. cash value:", cash,
			"\n5. total value:", final,
			"\n"
		)

	return final / init


def calc_ratio(curr, hi, lo, max_ratio, base=0.048):
	pct = (curr - lo) / (hi - lo)
	return max_ratio * (1 / (1 + exp(5 - 8 * pct)) + base)


def ratio_study(df, period=0):
	result = []
	x = []
	ratios = [x*0.1 for x in range(1, 121, 2)]

	for ratio in ratios:
		x.append(ratio)
		result.append(run_strat(df, ratio, to_plot=(round(ratio, 2) == 5.5), period=period, console=2))

	return x, result


def period_study(df, ratio=2.0):
	result = []
	x = []
	periods = [x for x in range(1, 21)]

	for p in periods:
		x.append(p)
		result.append(run_strat(df, ratio, to_plot=(p == 2), period=p, console=2))

	return x, result


def strat_shannon_1(latest_price=None, scan=True):
	df = read(API_KEY, SYM, RELOAD)
	# df = df[-10:]

	if latest_price:
		row = df.loc[df.index[-1]].copy()
		row['close'] = latest_price
		df.loc[pandas.to_datetime('today')] = row

		print(df['close'])

	if scan:
		x, result = ratio_study(df, 12)
		# x, result = period_study(df, 5.5)

		ht = df.iloc[[0, -1]]['close']
		naive = ht[-1] / ht[0]

		print("Buy-and-hold return:", naive, "\nRatio return:", [(x[i], result[i]) for i in range(len(x))])

		plt.plot(x, result)
		plt.show()

	else:
		vals = df['close']
		# print(df['close'][-1])
		r = calc_ratio(vals[-1], max(vals[-180:]), min(vals[-180:]), 6.0)
		print(r)

	return


if __name__ == '__main__':
	strat_shannon_1()
