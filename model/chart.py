import  matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
def chartAxis(val,val2,stockNumber,stockName):

    plt.plot(val)
    plt.plot(val2*len(val))
    plt.plot(val,'ro')
    plt.ylabel("成長幅度%")
    plt.xlabel("舊->新")
    plt.title(" 成長幅度%  "+stockName+"("+str(stockNumber)+")")
    plt.show()