# from urllib import request, parse
from datetime import datetime, timezone, timedelta
import bs4
import requests


debug = False


def get_url(ticket, p1, p2):
    base = "https://query1.finance.yahoo.com/v7/finance/download/" + ticket + "?period1=" + p1 + "&period2=" + p2 + "&interval=1d&events=history"
    return base


def crawl(ticket):
    start = convert(True)
    end = convert(False)

    url = get_url(ticket, start, end)
    raw = requests.get(url, allow_redirects=False)

    if debug:
        print(url, start, end)

    open("./data/" + ticket + ".csv", "wb").write(raw.content)


def convert(start):
    if start:
        d = datetime.utcnow() - timedelta(365)
    else:
        d = datetime.utcnow()

    if debug:
        print(d.year, d.month, d.day)

    return dt_to_epoch(d)


def dt_to_epoch(d):
    d1 = datetime(d.year, d.month, d.day, tzinfo=d.tzinfo)
    d2 = datetime(1970, 1, 1, tzinfo=d.tzinfo)

    delta = d1 - d2
    ts = int(delta.total_seconds())

    return str(ts)


def parse(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

    for link in soup.find_all('a'):
        print(link.get('href'))
