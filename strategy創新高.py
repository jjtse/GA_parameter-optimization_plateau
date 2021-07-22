import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns


# 策略描述 順勢-均線
# 資金:100萬
# 進場:收盤大於D日收盤的最高價
# 進場濾網:前20日收盤標準差小於vol
# 出場:收盤小於D日收盤的最低價

# vol:最小vol至最大vol,間距為(最大vol-最小vol)/15
# D:3至20

def history_data(file_name):
    std_20 = []

    csv_data = pd.read_csv(file_name, index_col=0, header=None)
    close = csv_data.iloc[0:len(csv_data), 3]
    std = close.rolling(20).std(ddof=0)

    for data in std:
        std_20.append(data)

    return close, std_20, std


def trade(file_name, new_day, std_filter):
    high_price = []
    low_price = []
    stk_close = []
    close = history_data(file_name)[0]
    std_20 = history_data(file_name)[1]

    for data in close:
        stk_close.append(data)

    # 位移一個順位後 計算創新高和創新低
    close = close.shift(1)
    New_high = close.rolling(new_day).max()
    New_low = close.rolling(new_day).min()

    for data in New_high:
        high_price.append(data)
    for data in New_low:
        low_price.append(data)

    # # # 交 易 流 程 # # #
    money = 1000000
    num_stock = 0
    return_list = []
    total_list = []

    for i in range(0, len(stk_close)):

        if num_stock == 0 and stk_close[i] > high_price[i] and std_20[i - 1] < std_filter:
            value = money // (stk_close[i] * 1000)  # 可買之張數
            buy_how_much = (stk_close[i] * 1000 * value) + math.ceil((stk_close[i] * 1000 * value * 0.001425))
            money = money - buy_how_much
            num_stock += value

        elif num_stock > 0 and stk_close[i] < low_price[i]:
            return_how_much = (stk_close[i] * 1000 * num_stock) - math.floor((stk_close[i] * 1000 * num_stock * 0.004425))
            money = return_how_much + money
            how_much = return_how_much - buy_how_much
            num_stock = 0
            return_list.append(how_much)

        profit = stk_close[i] * 1000 * num_stock
        total = profit + money
        total_list.append(total)
        # df = pd.DataFrame(total_list)
        # df.to_csv("total.csv")

    everyday_return_list = []

    for i in range(20, len(total_list)):
        everyday_return = (total_list[i] - total_list[i - 1]) / total_list[i - 1]
        everyday_return_list.append(everyday_return)

    return total_list  # 每日未實現+實現
    # return return_list  # 已實現損益


# 全部的total_list
def heatmap(file_name):
    std = history_data(file_name)[2]
    std_max = std.max()
    std_min = std.min()
    std_range = (std_max - std_min) / 15

    row = []
    col = []
    for i in range(3, 21):
        row.append(i)
    for j in np.arange(std_min, std_max, std_range):
        j = round(j, 1)
        col.append(j)

    result = []

    for i in range(3, 21):
        result.append([])
        for j in np.arange(std_min, std_max, std_range):
            j = round(j, 1)
            result[i - 3].append(trade(file_name, i, j))

    return result


if __name__ == '__main__':
    file = './data/3406_train.csv'
    # print(trade(file, 10, 16.4))