import io

import numpy as np
import bs4
import urllib.request as req
import lxml
from fake_useragent import UserAgent
import pandas as pd
from io import StringIO

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def chipInvestors(stock):
    url = "https://goodinfo.tw/tw/ShowBuySaleChart.asp?STOCK_ID=" + stock
    request = req.Request(url, headers={
        'User-Agent': UserAgent().random
    })
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')
    root = bs4.BeautifulSoup(data, 'lxml')
    # butDetail=StringIO(str(root.select_one("#divBuySaleDetail")))
    butDetail = root.select_one("#divBuySaleDetail")
    del_noTr = butDetail.find_all("tr", {"class": "bg_h2"})
    for tag in del_noTr:
        tag.decompose()

    if io.StringIO(str(butDetail)) is not None:
        foreign_holding = []
        foreign_holdingRate = []
        foreign_OBOS = []

        trust_OBOS = []
        dealer_OBOS = []

        chip_OBOS = []

        dfs = pd.read_html(io.StringIO(str(butDetail)))[0]

        for index in range(len(dfs)):
            foreign_OBOS.append(dfs.loc[index, 7])
            foreign_holding.append(dfs.loc[index, 8])
            foreign_holdingRate.append(dfs.loc[index, 9])
            trust_OBOS.append(dfs.loc[index, 12])
            dealer_OBOS.append(dfs.loc[index, 15])
            chip_OBOS.append(dfs.loc[index, 18])

        return foreign_OBOS, foreign_holding, foreign_holdingRate, trust_OBOS, dealer_OBOS, chip_OBOS


