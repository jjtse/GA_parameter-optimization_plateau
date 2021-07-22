import math
import time
import pandas as pd

from geneEncoding import geneEncoding
from selection import selection
from crossover import crossover
from crossover import mutation
from plateau_score import plateau_score


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

        # if decode > max_x_value:
        #     decode = max_x_value
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

        # if decode > max_y_value:
        #     decode = max_y_value
        y.append(decode)

    return y


# 計算所有種族的高原分數
def calobjValue(pop):
    obj_value = []
    temp1 = decode_x(pop)
    temp2 = decode_y(pop)
    for i in range(len(temp1)):
        if temp1[i] > max_x_value or temp2[i] > max_y_value:
            obj_value.append(0)

        else:
            obj_value.append(plateau_score(df_list, temp2[i], temp1[i], 5, 1))  # 高原分數

    return obj_value


# 選出最佳個體的基因和高原分數
def best(pop, obj_value):
    best_individual = []
    best_fit = obj_value[0]
    for i in range(1, len(pop)):
        if obj_value[i] > best_fit:
            best_fit = obj_value[i]
            best_individual = pop[i]
        if best_fit == obj_value[0]:
            best_individual = pop[0]
    return [best_individual, best_fit]


# 解碼最佳個體
def binary(best_individual):
    x_power = 3
    x = 0
    for j in range(4):
        x += best_individual[j] * (math.pow(2, x_power))
        x = int(x)
        x_power -= 1
        if x > max_x_value:
            x = max_x_value

    y_power = 4
    y = 0
    for j in range(4, len(best_individual)):
        y += best_individual[j] * (math.pow(2, y_power))
        y = int(y)
        y_power -= 1
        if y > max_y_value:
            y = max_y_value

    x = column_list[int(x)]
    y = index_list[int(y)]

    return x, y


if __name__ == '__main__':

    time_start = time.time()

    heatmap_df = pd.read_csv("3406_shapre_ratio.csv", index_col=0)
    df_list = heatmap_df.values.tolist()
    index_list = list(pd.to_numeric(heatmap_df.index))
    column_list = list(pd.to_numeric(heatmap_df.columns))

    # 編碼的max_value設定
    max_x_value = len(column_list) - 1
    max_y_value = len(index_list) - 1

    pop_size = 12  # 种群数量
    x_chromosome = 4
    y_chromosome = 5
    chromosome_length = x_chromosome + y_chromosome  # 染色體長度
    results = []  # 儲存每一代的最優解
    crossover_probability = 0.6  # 交配概率
    mutation_probability = 0.1  # 变异概率

    n = 0
    while n < 10:
        # 編碼
        pop = geneEncoding(pop_size, chromosome_length)

        for i in range(pop_size):
            obj_value = calobjValue(pop)  # 個體評價
            # print(best(pop, obj_value))
            best_individual, best_fit = best(pop, obj_value)  # 最佳個體的基因和高原分數
            results.append([best_fit, binary(best_individual)])
            selection(pop, obj_value)
            crossover(pop, crossover_probability)  # 交配
            mutation(pop, mutation_probability)  # 變異
        results.sort()
        print(results)
        print("高原分數 = ", results[-1][0], "座標 = ", results[-1][1])

        time_end = time.time()
        print('time elapsed: ' + str(time_end - time_start) + ' seconds')

        n += 1
