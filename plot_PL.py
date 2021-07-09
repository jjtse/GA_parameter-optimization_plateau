import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from strategy import *
from plateau_score import plateau_score

file_name = "2912.csv"
df_list = pd.read_csv("2912_shapre_ratio.csv", index_col=0)

csv_data = pd.read_csv(file_name, index_col=0)
max_date = date_index = list(csv_data.index.values)
max_date = pd.to_datetime(max_date)
train_total = [trade(file_name, 18, 1.9), trade(file_name, 18, 1.9), trade(file_name, 18, 2.7)]
gray_train_total = sharpe(file_name)

file_name = "2912_test.csv"
csv_data = pd.read_csv(file_name, index_col=0)
date_index = list(csv_data.index.values)
date_index = pd.to_datetime(date_index)
test_total = [trade(file_name, 18, 1.9), trade(file_name, 18, 1.9), trade(file_name, 18, 2.7)]
test_total = np.array(test_total)
gray_test_total = sharpe(file_name)
gray_test_total = np.array(gray_test_total)

for i in range(3):
    test_total[i] = test_total[i] - 1000000 + train_total[i][len(train_total[i]) - 1]

fig, ax1 = plt.subplots()
for i in range(0, 18, 2):
    for j in range(0, 15, 2):
        ax1.plot(max_date, gray_train_total[i][j], 'lightgray')
        gray_test_total[i][j] = gray_test_total[i][j] - 1000000 + gray_train_total[i][j][len(gray_train_total[i][j]) - 1]
        ax1.plot(date_index, gray_test_total[i][j], 'lightgray')

# train
line1, = ax1.plot(max_date, train_total[0], 'darkorange', linewidth=2.5, label='Best Sharpe')
line2, = ax1.plot(max_date, train_total[1], 'dodgerblue', linewidth=2.5, label='Best Plateau Score')
line3, = ax1.plot(max_date, train_total[2], 'green', linewidth=2.5, label='GA Plateau Score')
# test
ax1.plot(date_index, test_total[0], 'darkorange', linewidth=2.5)
ax1.plot(date_index, test_total[1], 'dodgerblue', linewidth=2.5)
ax1.plot(date_index, test_total[2], 'green', linewidth=2.5)

plt.legend(handles=[line1, line2, line3], loc='upper left', prop={'size': 8})

# ax1.plot(max_date, train_total, 'dodgerblue', linewidth=2.5, label='Training')
# ax1.plot(date_index, test_total, 'darkorange', linewidth=2.5, label='Testing')

plt.axvspan(max_date[0], max_date[-1], facecolor='skyblue', alpha=0.15)
plt.axvspan(date_index[0], date_index[-1], facecolor='salmon', alpha=0.15)
plt.grid()
# plt.vlines(x=min(date_index), ymin=min(train_total), ymax=max(test_total), colors='r',
#            linestyles='dashed', label='Testing Start')

plt.xlabel('Date')
plt.ylabel('equity curve')
plt.show()

# print(trade(18, 1.9))
