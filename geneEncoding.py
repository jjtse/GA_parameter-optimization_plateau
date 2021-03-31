import random
import math

max_x_value = 14
max_y_value = 17

def geneEncoding(pop_size, chromosome_length):
    pop = [[]]
    for i in range(pop_size):
        temp = []
        for j in range(chromosome_length):
            temp.append(random.randint(0, 1))
        pop.append(temp)

    return pop[1:]
    
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

        if decode > max_x_value:
            decode = max_x_value
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

        if decode > max_y_value:
            decode = max_y_value
        y.append(decode)

    return y

if __name__ == '__main__':
    pop_size = 50		# 种群数量
    x_chromosome = 4
    y_chromosome = 5
    chromosome_length = x_chromosome + y_chromosome		# 染色体长度
    pop = geneEncoding(pop_size, chromosome_length)
    print(decode_x(pop))
    print(decode_y(pop))

