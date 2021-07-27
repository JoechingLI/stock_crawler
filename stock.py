import requests
import re
from bs4 import BeautifulSoup
import traceback


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('section').find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r'[S][HZ]\d{6}', href))
        except:
            continue


def getStockInfo(lst, stockURL, fpath):
    for stock in lst:
        if len(stock):
            try:
                url = stockURL + stock[0]
                html = getHTMLText(url)
                if html == '':
                    continue
                infoDict = {}
                soup = BeautifulSoup(html, "html.parser")
                price = soup.find('div', attrs={'class': 's_price'}).find_all('em')[0].string
                infoDict['股票代码'] = stock[0]
                infoDict['股票价格'] = price

                with open(fpath, 'a', encoding='utf-8') as f:
                    f.write(str(infoDict) + '\n')
            except:
                traceback.print_exc()
                continue


def main():
    stock_list_url = 'https://hq.gucheng.com/gpdmylb.html'
    stock_info_url = 'https://hq.gucheng.com/'
    output_file = 'StockInfo4.txt'
    slist = []
    getHTMLText(stock_list_url)
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)


main()