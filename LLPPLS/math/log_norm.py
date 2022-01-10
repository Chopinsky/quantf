from math import exp
from scipy.stats import lognorm


def cdf(x: float, mean: float, sigma: float) -> float:
	return lognorm.cdf(x, sigma, 0, exp(mean))


def pdf(x: float, mean: float, sigma: float) -> float:
	return lognorm.pdf(x, sigma, 0, exp(mean))
