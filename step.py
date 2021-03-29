import math
import pandas as pd
import numpy as np

import strategy


# 多維參數夏普比率計算
def sharpe():
    result = []

    for i in range(3, 21):
        result.append([])
        for j in np.arange(std_min, std_max, std_range):
            j = round(j, 1)
            result[i-3].append(strategy.trade(i, j))
            
    # a=pd.DataFrame(result)
    # a.index = row
    # a.columns = col
    # #print(a)

    return result


# 高原分數計算
def plateau_score(short_ma, std_filter, n, m):

    # 取得sharpe ratio放入二維陣列
    sharpe_list = sharpe()

    # 暫存座標
    x1 = y1 = 0
    
    for i in range(0, len(sharpe_list)):
        for j in range(0, len(sharpe_list[i])):
            if sharpe_list[i][j] == strategy.trade(short_ma, std_filter):
                x1, y1 = i, j
    
    score = 0  # 權重高原分數
    cells = []  # n步的格子數
    match = []  # 符合高原標準值的step
    match_count = 0  # 紀錄n步符合個數
    cells_count = 0  # 紀錄cells個數

    for i in range(x1-n, x1+n+1):
        for j in range(y1-n, y1+n+1):

            if i >= 0 and j >= 0 and i <= len(sharpe_list)-1 and j <= len(sharpe_list[0])-1:
                step = abs(x1-i)+abs(y1-j)
                cells.append(step)

                if step <= n and sharpe_list[i][j]>=m:
                    # print("n步?",step,"座標:",i,j,sharpe_list[i][j])
                    match.append(step)

    for k in range(n+1):
        match_count = match_count + match.count(k)
        cells_count = cells_count + cells.count(k)
        print(match_count, "/", cells_count)
        score = score+(match_count/cells_count)

    return score   


def score_heatmap():
    score = []

    for i in range(3, 21):
        score.append([])
        for j in np.arange(std_min, std_max, std_range):
            j = round(j, 1)
            score[i-3].append(plateau_score(i, j, 5, 0.5)) #高原分數MA,std,n步,sharpe
            print("score_heatmap here:", i, j)
    
    # a=pd.DataFrame(score)
    # a.index = row
    # a.columns = col
    # print(a)

    return


if __name__ == '__main__':
    
    close = strategy.close
    std=close.rolling(20).std(ddof=0)
    
    strategy.stkclose = []
    strategy.stdvalue = []
    for data in close:
        strategy.stkclose.append(data)
    for data in std:
        strategy.stdvalue.append(data)
    
    std_max = std.max()
    std_min = std.min()
    std_range = (std_max-std_min)/15

    row = []
    col = []
    for i in range(3, 21):
        row.append(i)
    for j in np.arange(std_min, std_max, std_range):
        j = round(j, 1)
        col.append(j)

    # score_heatmap()
    # plateau_score(20,0.4,2,0.03)
    print(plateau_score(17, 2.7, 4, 0.1))