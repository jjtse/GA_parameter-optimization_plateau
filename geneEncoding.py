# 0.0 coding:utf-8 0.0
import random

def geneEncoding(pop_size, chromosome_length):
    pop = [[]]
    for i in range(pop_size):
        temp = []
        for j in range(chromosome_length):
            temp.append(random.randint(0, 1))
        pop.append(temp)

    return pop[1:]


if __name__ == '__main__':
    pop_size = 50		# 种群数量
    x_chromosome = 4
    y_chromosome = 5
    chromosome_length = x_chromosome + y_chromosome		# 染色体长度
    pop = geneEncoding(pop_size, chromosome_length)
    print(pop)

