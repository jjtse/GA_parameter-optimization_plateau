import random
from geneEncoding import geneEncoding

def sum(fit_value):
	total = 0
	for i in range(len(fit_value)):
		total += fit_value[i]
	return total


def cumsum(fit_value):
	for i in range(len(fit_value)-2, -1, -1):
		t = 0
		j = 0
		while(j <= i):
			t += fit_value[j]
			j += 1
		fit_value[i] = t
		fit_value[len(fit_value)-1] = 1  # 最後收斂為1


def selection(pop, fit_value):
	newfit_value = []
	total_fit = sum(fit_value)  # 適合度總和
	for i in range(len(fit_value)):
		if total_fit != 0:
			newfit_value.append(fit_value[i] / total_fit)  # 重要性占比
		else:
			newfit_value.append(0)
	
	cumsum(newfit_value)  # 累加概率
	random_number = []  # 隨機產生0-1之間的亂數
	for i in range(len(pop)):
		random_number.append(random.random())
	random_number.sort()
	fitin = 0
	newin = 0
	newpop = pop
	# 轉輪盤選擇法
	# 如果累加概率>隨機亂數(從最小的開始比對)，則保留原本的基因
	while newin < len(pop):
		if(random_number[newin] < newfit_value[fitin]):
			newpop[newin] = pop[fitin]
			newin = newin + 1
		else:
			fitin = fitin + 1
	pop = newpop


if __name__ == '__main__':
	pass