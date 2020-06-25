from urllib import request, parse
import bs4


def crawl():
    resp = request.urlopen('https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC')
    content = resp.read()
    parse(content)


def parse(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')

    for link in soup.find_all('a'):
        print(link.get('href'))
