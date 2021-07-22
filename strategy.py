import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns


# 策略描述 順勢-均線
# 資金:100萬
# 進場:收盤大於D日移動平均線
# 進場濾網:前20日收盤標準差小於vol
# 出場:收盤小於D日移動平均線

# vol:最小vol至最大vol,間距為(最大vol-最小vol)/15
# D:3至20

def history_data(file_name):
    csv_data = pd.read_csv(file_name, index_col=0, header=None)
    date_index = list(csv_data.index.values)
    close = csv_data.iloc[0:len(csv_data), 3]
    std = close.rolling(20).std(ddof=0)
    stkclose = []
    stdvalue = []

    for data in close:
        stkclose.append(data)
    for data in std:
        stdvalue.append(data)

    return stkclose, stdvalue, close, std


def trade(file_name, ma_value, std_filter):
    stkclose = history_data(file_name)[0]
    stdvalue = history_data(file_name)[1]
    close = history_data(file_name)[2]

    maprice = []
    MA = close.rolling(ma_value).mean()

    for data in MA:
        maprice.append(data)

    # # # 交 易 流 程 # # #
    money = 1000000
    num_stock = 0
    return_list = []
    total_list = []

    for i in range(0, len(stkclose)):

        if num_stock == 0 and stkclose[i] > maprice[i - 1] and stdvalue[i - 1] < std_filter:
            buyvalue = money // (stkclose[i] * 1000)  # 可買之張數
            buy_how_much = (stkclose[i] * 1000 * buyvalue) + math.ceil((stkclose[i] * 1000 * buyvalue * 0.001425))
            money = money - buy_how_much
            num_stock += buyvalue

        elif num_stock > 0 and stkclose[i] < maprice[i - 1]:
            return_how_much = (stkclose[i] * 1000 * num_stock) - math.floor((stkclose[i] * 1000 * num_stock * 0.004425))
            money = return_how_much + money
            how_much = return_how_much - buy_how_much
            num_stock = 0
            return_list.append(how_much)

        profit = stkclose[i] * 1000 * num_stock
        total = profit + money
        total_list.append(total)
        # df = pd.DataFrame(total_list)
        # df.to_csv("total.csv")

    everyday_return_list = []

    for i in range(20, len(total_list)):
        everyday_return = (total_list[i] - total_list[i - 1]) / total_list[i - 1]
        everyday_return_list.append(everyday_return)

    return total_list, return_list


if __name__ == '__main__':
    file = './data/2912.csv'
    print(trade(file, 18, 1.9))
