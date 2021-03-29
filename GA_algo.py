import math

from geneEncoding import geneEncoding
from sharpe import trade
from sharpe import plateau_score

pop_size = 100  # 种群数量
x_chromosome = 4
y_chromosome = 5
chromosome_length = x_chromosome + y_chromosome  # 染色体长度
results = [[]]  # 存储每一代的最优解，N个二元组

# 編碼
pop = geneEncoding(pop_size, chromosome_length)


# print (pop[0])

# 解碼X軸
def decode_x(pop):
    x = []
    for i in range(len(pop)):
        decode = 0
        x_power = 3  # 二的三次方
        for j in range(0, 4):
            decode += pop[i][j] * (math.pow(2, x_power))
            decode = int(decode)
            x_power -= 1
        x.append(decode)

    return x


# 解碼Y軸
def decode_y(pop):
    y = []
    for i in range(len(pop)):
        decode = 0
        y_power = 4

        for j in range(4, 9):
            decode += pop[i][j] * (math.pow(2, y_power))
            decode = int(decode)
            y_power -= 1
        y.append(decode)

    return y


# 計算shapre ratio
def calobjValue(pop):
    temp1 = []
    temp2 = []
    obj_value = []
    temp1 = decode_x(pop)
    temp2 = decode_y(pop)
    for i in range(len(temp1)):
        obj_value.append(plateau_score(temp1[i], temp2[i]))
    return obj_value


# 淘汰<0
# def calfitValue(obj_value):

#     fit_value = []
#     for i in range(len(obj_value)):
#         if(obj_value[i] > 0 or obj_value[i] != None):
#             temp = obj_value[i]
#         elif(obj_value[i] < 0):
#             temp = 0.0
#         fit_value.append(temp)

#     print(fit_value)
#     return fit_value

def best(pop, fit_value):
    best_individual = []
    best_fit = fit_value[0]
    for i in range(1, len(pop)):
        if (fit_value[i] > best_fit):
            best_fit = fit_value[i]
            best_individual = pop[i]
        if (best_fit == fit_value[0]):
            best_individual = pop[0]
    return [best_individual, best_fit]


def binary_short(b):
    short_power = 2
    t = 0
    for j in range(3):
        t += b[j] * (math.pow(2, short_power))
        short_power -= 1

    return t + 3


def binary_long(b):
    long_power = 3
    t = 0
    for j in range(3, len(b)):
        t += b[j] * (math.pow(2, long_power))
        long_power = long_power - 1
    return t + 15


if __name__ == '__main__':
    # print(decodeshort(pop))
    # print(decodelong(pop))
    # print(calobjValue(pop))
    obj_value = calobjValue(pop)
    # fit_value = calfitValue(obj_value)
    # print(best(pop, obj_value))
    best_individual, best_fit = best(pop, obj_value)
    print("最佳染色體:")
    print(best_individual)
    print("高原分數:%.0f" % (best_fit))
    print("短週期MA:%.0f" % (binary_short(best_individual)))
    print("長週期MA:%.0f" % (binary_long(best_individual)))
    # results.append([best_fit, binary_long(best_individual)])
    # print(results)