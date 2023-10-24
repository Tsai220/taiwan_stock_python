import urllib.request as req
import bs4
import pandas
import lxml
from io import StringIO
import model.eps as epsRate
import model.chart as chart
import time
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

def search(stockNumber):
    url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID="+str(stockNumber)
    request = req.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    })
    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')

    root = bs4.BeautifulSoup(data, "lxml")
    catchTable = StringIO(str(root.select_one('#tblFinDetail')))  # 先將html轉str在轉StringIO來變成可處理文本
    dfs = pandas.read_html(catchTable)[0]

    epsRateOUT = epsRate.eps(dfs.loc[6, '2023Q2':'2021Q1'][::-1])
    chart.chartAxis(epsRateOUT[0],epsRateOUT[1],stockNumber)
    print(epsRateOUT)
    time.sleep(3)
search("2605")
