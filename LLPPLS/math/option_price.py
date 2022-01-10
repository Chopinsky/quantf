from typing import Callable
import time
import random


def mc_integral(formula: Callable, val: float, mean: float, sigma: float, count: int = 10000) -> float:
	"""
	Calculate the integral using Mont-Carlo simulations

	:param formula: the pdf integral function
	:param val:     the value to evaluate for the [0, val) integral range for CDF, usually ln(x) of
									the x value to be evaluated
	:param mean:    mean value of ln(x)
	:param sigma:   1 sigma of ln(x)
	:param count:   number of iterations
	:return:        the mont-carlo integral
	"""

	s = 0.0
	random.seed(int(time.time()))

	# randomize the walk to estimate the integral sum
	for _ in range(count):
		s += formula(val * random.random(), mean, sigma)

	# normalize the result
	s = s * val / float(count)

	return s
