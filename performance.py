from strategy創新高 import *
# from strategy import *
from plateau_score import plateau_score
from matplotlib.patches import Rectangle

# ----------------------------#
# 注意import的project          |
# history return 的東西不同     |
# read file                   |
# 夏普或獲利因子                 |
# ----------------------------#


def sharpe(total_list):
    # # # 績 效 計 算 # # #
    # 夏普比率 = 每日報酬平均/每日報酬標準差

    everyday_return_list = []

    for i in range(20, len(total_list)):
        everyday_return = (total_list[i] - total_list[i - 1]) / total_list[i - 1]
        everyday_return_list.append(everyday_return)

    std = np.std(everyday_return_list, ddof=0)

    if std == 0:
        return 0
    else:
        average = np.mean(everyday_return_list)
        sharpe_ratio = np.round((average / std) * (252 ** (1 / 2)), 3)
        # profit_factor = sum(win_list) / abs(sum(lose_list))
        return sharpe_ratio


def profit_factor(total_list):
    everyday_return_list = []

    for i in range(20, len(total_list)):
        everyday_return = (total_list[i] - total_list[i - 1]) / total_list[i - 1]
        everyday_return_list.append(everyday_return)
    win_list = []
    lose_list = []

    for i in everyday_return_list:
        if i >= 0:
            win_list.append(i)
        else:
            lose_list.append(i)

    if abs(sum(lose_list)) != 0:
        PF = sum(win_list) / abs(sum(lose_list))
    else:
        PF = 0

    return PF


# 多維參數夏普比率計算
# def heatmap(file_name):
#     std = history_data(file_name)[3]
#     std_max = std.max()
#     std_min = std.min()
#     std_range = (std_max - std_min) / 15
#
#     row = []
#     col = []
#     for i in range(3, 21):
#         row.append(i)
#     for j in np.arange(std_min, std_max, std_range):
#         j = round(j, 1)
#         col.append(j)
#
#     result = []
#
#     for i in range(3, 21):
#         result.append([])
#         for j in np.arange(std_min, std_max, std_range):
#             j = round(j, 1)
#             unrealized = trade(file, i, j)
#             result[i - 3].append(sharpe(unrealized))
#
#     a = pd.DataFrame(result)
#     a.index = row
#     a.columns = col
#     # print(a)
#     # a.to_csv("3406_shapre_ratio.csv")
#     sns.heatmap(a, annot=True, fmt='.3f', annot_kws={"fontsize": 5}, cmap="OrRd")
#
#     plt.title("performance")
#     plt.show()
#
#     return result

# 合併圖
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
            total = trade(file_name, i, j)
            result[i - 3].append(sharpe(total))

    a = pd.DataFrame(result)
    a.index = row
    a.columns = col
    print(a)
    ax = sns.heatmap(a, annot=True, fmt='.3f', annot_kws={"fontsize": 5}, cmap="OrRd")

    score = []
    df_list = a.values.tolist()

    for i in range(len(df_list)):
        score.append([])
        for j in range(len(df_list[0])):
            score[i].append(plateau_score(df_list, i, j, 5, 1))  # 高原分數(dataframe, MA, std, n步, 績效)

    score_df = pd.DataFrame(score)
    score_max = score_df.max().max()
    print(score_df)

    for i in range(len(df_list)):
        for j in range(len(df_list[0])):
            if score[i][j] == score_max:
                ax.add_patch(Rectangle((j, i), 1, 1, fill=False, edgecolor='yellow', lw=2))

    score_df.index = row
    score_df.columns = col
    # print(a)
    # sns.heatmap(a, annot=True, fmt='.3f', annot_kws={"fontsize": 5}, cmap="OrRd")
    #
    plt.title("performance")
    plt.show()

    return result


if __name__ == '__main__':
    # file = './data/2912.csv'
    file = './data/3406_train.csv'
    heatmap(file)

