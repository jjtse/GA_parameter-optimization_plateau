# 0.0 coding:utf-8 0.0
# 交配

import random


def crossover(pop, probability):
    pop_len = len(pop)
    for i in range(pop_len - 1):
        if(random.random() < probability):
            cpoint = random.randint(0,len(pop[0]))
            temp1 = []
            temp2 = []
            temp1.extend(pop[i][0:cpoint])
            temp1.extend(pop[i+1][cpoint:len(pop[i])])
            temp2.extend(pop[i+1][0:cpoint])
            temp2.extend(pop[i][cpoint:len(pop[i])])
            pop[i] = temp1
            pop[i+1] = temp2

def mutation(pop, probability):
    px = len(pop)
    py = len(pop[0])
    
    for i in range(px):
        if(random.random() < probability):
            mpoint = random.randint(0, py-1)
            if(pop[i][mpoint] == 1):
                pop[i][mpoint] = 0
            else:
                pop[i][mpoint] = 1


if __name__ == '__main__':
    pass
