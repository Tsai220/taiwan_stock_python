import urllib.request as req
import bs4
import pandas
import lxml
from io import StringIO
import model.eps as epsRate
import model.chart as chart
import time

stockTypeTxt = "\n0.全部\n01.水泥工業\n02.食品工業\n03.塑膠工業\n04.紡織纖維\n05.電機機械\n06.電器電纜\n08.玻璃陶瓷\n09.造紙工業\n10.鋼鐵工業\n11.橡膠工業\n12.汽車工業\n13.電子工業\n14.建材營造業\n15.航運業\n16.觀光餐旅\n17.金融保險業\n18.貿易百貨業\n19.綜合\n20.其他業\n21.化學工業\n22.生技醫療業\n23.油電燃氣業\n24.半導體業\n25.電腦及週邊設備業\n26.光電業\n27.通信網路業\n28.電子零組件業\n29.電子通路業\n30.資訊服務業\n31.其他電子業\n32.文化創意業\n33.農業科技業\n34.電子商務\n35.綠能環保\n36.數位雲端\n37.運動休閒\n38.居家生活"
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

print('投資一定有風險，投資有賺有賠，該程式僅為分析之用，僅供參考')
print(
    '-----\n查詢股票市場別(請輸入類別)' + '\n1.上市股票' + '\n2.上櫃股票' + '\n3.上市和上櫃股票' + '\n4.輸入股票代碼' + '\n5.結束程式')
choose = str(input("請輸入類別: "))


def search(stockNumber, market, issueType, industry_code):
    market = market
    issueType = issueType
    industry_code = industry_code
    for index, stock in enumerate(stockNumber):
        try:
            url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=" + stock + "&stockname=&isincode=&market=" + market + "&issuetype=" + issueType + "&industry_code=" + industry_code + "&Page=1&chklike=Y"
            request = req.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
            })
            with req.urlopen(request) as response:
                data = response.read().decode('MS950')

            root = bs4.BeautifulSoup(data, "lxml")
            StockInfo = StringIO(str(root.select_one('.h4')))

            if StockInfo is not None:
                dfs = pandas.read_html(StockInfo)[0]

                analyze(stockNumber=dfs.loc[1, 2], stockName=dfs.loc[1, 3])
                time.sleep(1)

        except ValueError:
            print(stock + " 未知股票代號")

            continue


def analyze(stockNumber, stockName):

    try:
        url = "https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=" + str(stockNumber)
        request = req.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        })
        with req.urlopen(request) as response:
            data = response.read().decode('utf-8')

        root = bs4.BeautifulSoup(data, "lxml")

        catchTable = StringIO(str(root.select_one('#tblFinDetail')))  # 先將html轉str在轉StringIO來變成可處理文本
        if catchTable is not None:
            dfs = pandas.read_html(catchTable)[0]

            epsRateOUT = epsRate.eps(dfs.loc[6, '2023Q2':'2021Q1'][::-1])
            chart.chartAxis(epsRateOUT[0], epsRateOUT[1], stockNumber, stockName)
            print(stockNumber,epsRateOUT)
            time.sleep(5)

    except ValueError:
        print(stockNumber + " 未知股票代號")


if choose == '3':
    print("------" + stockTypeTxt)
    enter = str(input("輸入產業別: "))

elif choose == '4':
    stocks = []
    while True:
        enter = str(input("輸入股票代碼(輸入完畢請按Enter): "))
        if enter == "n" or enter == "no" or enter == "":
            search(stockNumber=stocks, market='', issueType='', industry_code='')
            break
        elif enter is not None and enter != "n" and enter != "no":
            stocks.append(enter)
        else:
            print("結束程式")
            break
elif choose == '5':
    print("結束程式")
