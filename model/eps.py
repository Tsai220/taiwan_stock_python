import pandas
import numpy as np


def eps(Alleps):
    obj = Alleps.to_numpy()
    objArr = []
    growth = []

    # 成長幅度% = ((新值 - 舊值) / 舊值) * 100
    for index, val in enumerate(obj):
        objArr.append(float(val))#[舊到新]

        if index == 0:
            growth.append(0.0)
        elif index > 0:
            if objArr[index - 1]==0:
                growth.append(float(0))
            else:
                calc = (((objArr[index]) - (objArr[index - 1])) /(objArr[index - 1])) * 1
                calc_format = "{:.4f}".format(calc)
                growth.append(float(calc_format))
        else:
            print("Has Error")
    growth.pop(0)
    calcAvg = float(np.nansum(growth) / (len(growth)))
    growthAvg =[ float("{:.4f}".format(calcAvg))]

    return growth, growthAvg
