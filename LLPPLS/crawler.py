# from urllib import request, parse
from datetime import datetime, timezone, timedelta
import bs4
import requests


def get_url(ticket, p1, p2):
    base = "https://query1.finance.yahoo.com/v7/finance/download/" + ticket + "?period1=" + p1 + "&period2=" + p2 + "&interval=1d&events=history"
    return base


def crawl(ticket):
    start = convert(True)
    end = convert(False)

    url = get_url(ticket, start, end)
    raw = requests.get(url, allow_redirects=False)

    open("./data/" + ticket + ".csv", "wb").write(raw.content)


def convert(start):
    if start:
        d = datetime.now() - timedelta(365)
    else:
        d = datetime.now() - timedelta(1)

    # print(dt_to_epoch(d1))
    # print(dt_to_epoch(d2))

    return dt_to_epoch(d)


def dt_to_epoch(d):
    # create 1,1,1970 in same timezone as d1
    # d1 = datetime.utcnow()
    # d1 = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    d2 = datetime(1970, 1, 1, tzinfo=d.tzinfo)
    delta = d - d2
    ts = int(delta.total_seconds())

    return str(ts)


def parse(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    print(soup.prettify())

    for link in soup.find_all('a'):
        print(link.get('href'))
