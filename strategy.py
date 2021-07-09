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
    csv_file = file_name
    csv_data = pd.read_csv(csv_file, index_col=0)
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
    std = history_data(file_name)[3]

    maprice = []
    MA = close.rolling(ma_value).mean()

    for data in MA:
        maprice.append(data)

    # # # 交 易 流 程 # # #
    money = 1000000
    num_stock = 0
    PF = []
    win_list = []
    lose_list = []
    total_list = []

    for i in range(0, len(stkclose)):

        if num_stock == 0 and stkclose[i] > maprice[i - 1] and stdvalue[i - 1] < std_filter:
            buyvalue = money // (stkclose[i] * 1000)  # 可買之張數
            buy_how_much = (stkclose[i] * 1000 * buyvalue) - math.ceil((stkclose[i] * 1000 * buyvalue * 0.001425))
            money = money - buy_how_much
            num_stock += buyvalue

        elif num_stock > 0 and stkclose[i] < maprice[i - 1]:
            return_how_much = (stkclose[i] * 1000 * num_stock) - math.floor((stkclose[i] * 1000 * num_stock * 0.004425))
            money = return_how_much + money
            how_much = return_how_much - buy_how_much
            num_stock = 0
            PF.append(how_much)

        # if how_much > 0:
        #     win_how_much += how_much
        #
        # elif how_much < 0:
        #     loss_how_much += how_much
        profit = stkclose[i] * 1000 * num_stock
        total = profit + money
        total_list.append(total)
        # df = pd.DataFrame(total_list)
        # df.to_csv("total.csv")
    for i in PF:
        if i >= 0:
            win_list.append(i)
        else:
            lose_list.append(i)

    # # # 績 效 計 算 # # #
    # 每日報酬平均/每日報酬標準差

    everyday_return_list = []

    for i in range(20, len(total_list)):
        everyday_return = (total_list[i] - total_list[i - 1]) / total_list[i - 1]
        everyday_return_list.append(everyday_return)

    return total_list

    # std = np.std(everyday_return_list, ddof=0)
    #
    # if std == 0:
    #     return 0
    # else:
    #     average = np.mean(everyday_return_list)
    #     sharpe = np.round((average / std) * (252 ** (1 / 2)), 3)
    #     profit_factor = sum(win_list) / abs(sum(lose_list))
    #     return sharpe


# 多維參數夏普比率計算
def sharpe(file_name):
    std = history_data(file_name)[3]
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

    a = pd.DataFrame(result)
    a.index = row
    a.columns = col
    # print(a)
    # a.to_csv("2912_shapre_ratio.csv")
    # sns.heatmap(a, annot=True, fmt='.3f', annot_kws={"fontsize": 5}, cmap="OrRd")
    # plt.title("performance")
    # plt.show()

    return result


if __name__ == '__main__':
    # sharpe()
    print(trade(18, 1.9))
