import math
import pandas as pd

from geneEncoding import geneEncoding
from selection import selection
from plateau_score import plateau_score

pop_size = 50  # 种群数量
x_chromosome = 4
y_chromosome = 5
chromosome_length = x_chromosome + y_chromosome  # 染色體長度
results = []  # 儲存每一代的最優解
pc = 0.6			# 交配概率
pm = 0.01           # 变异概率

# 編碼
pop = geneEncoding(pop_size, chromosome_length)

# 解碼X軸:column
def decode_x(pop):
    x = []
    for i in range(len(pop)):
        decode = 0
        x_power = 3  # 二的三次方
        for j in range(0, 4):
            decode += pop[i][j] * (math.pow(2, x_power))
            decode = int(decode)
            x_power -= 1

        if decode > max_x_value:
            decode = max_x_value
        x.append(decode)

    return x


# 解碼Y軸:index
def decode_y(pop):
    y = []
    for i in range(len(pop)):
        decode = 0
        y_power = 4

        for j in range(4, 9):
            decode += pop[i][j] * (math.pow(2, y_power))
            decode = int(decode)
            y_power -= 1

        if decode > max_y_value:
            decode = max_y_value
        y.append(decode)

    return y

# 計算所有種族的高原分數
def calobjValue(pop):
    temp1 = []
    temp2 = []
    obj_value = []
    temp1 = decode_x(pop)
    temp2 = decode_y(pop)
    for i in range(len(temp1)):
        obj_value.append(plateau_score(df_list, temp2[i], temp1[i], 3, 0.1))
    return obj_value 

# 選出最佳個體的基因和高原分數
def best(pop, obj_value):
    best_individual = []
    best_fit = obj_value[0]
    for i in range(1, len(pop)):
        if (obj_value[i] > best_fit):
            best_fit = obj_value[i]
            best_individual = pop[i]
        if (best_fit == obj_value[0]):
            best_individual = pop[0]
    return [best_individual, best_fit]


def binary(best_individual):
    x_power = 3
    x = 0
    for j in range(4):
        x += best_individual[j] * (math.pow(2, x_power))
        x_power -= 1
    
    y_power = 4
    y = 0
    for j in range(4, len(best_individual)):
        y += best_individual[j] * (math.pow(2, y_power))
        y_power = y_power - 1
    return x, y

if __name__ == '__main__':

    heatmap_df = pd.read_csv("2912_shapre_ratio.csv", index_col=0)
    df_list = heatmap_df.values.tolist()
    index_list = list(heatmap_df.index.values)
    column_list = list(heatmap_df.columns)
    # 編碼的max_value設定
    max_x_value = len(column_list)-1
    max_y_value = len(index_list)-1

    obj_value = calobjValue(pop)  # 個體評價
    print(best(pop, obj_value))
    best_individual, best_fit = best(pop, obj_value)  # 最佳個體的基因和高原分數
    results.append([best_fit, binary(best_individual)])
    print(results)
    