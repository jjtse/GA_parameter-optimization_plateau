import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


# 單點高原分數計算(dataframe, MA, std, n步, 勝率)
def plateau_score(df_list, index, columns, n, m):

    # 座標
    x1 = index
    y1 = columns

    score = 0 #權重高原分數
    cells=[] #n步的格子數
    match = [] #符合高原標準值的step
    match_count = 0 #紀錄n步符合個數
    cells_count = 0 #紀錄cells個數

    for i in range(x1-n,x1+n+1):
        for j in range(y1-n,y1+n+1):

            if 0 <= i <= len(df_list)-1 and 0 <= j <= len(df_list[0])-1:
                step = abs(x1-i)+abs(y1-j)
                cells.append(step)

                if step <= n and df_list[i][j]>=m:
                    match.append(step)
            
    for k in range(n+1):
        match_count = match_count + match.count(k)
        cells_count = cells_count + cells.count(k)
        score = score+(match_count/cells_count)

    return round(score, 5)

# 整個df的高原分數
def score_heatmap(heatmap_df):

    score = []
    df_list = heatmap_df.values.tolist()

    for i in range(len(df_list)):
        score.append([])
        for j in range(len(df_list[0])):
            score[i].append(plateau_score(df_list, i, j, 3, 0.1))  # 高原分數(dataframe, MA, std, n步, 勝率)


    score_df = pd.DataFrame(score)
    score_df.index = index_list
    score_df.columns = column_list
    print(score_df)
    # sns.heatmap(score_df,cmap="Greens")
    # plt.title("plateau_score")
    # plt.show()

    score_max = score_df.max().max()
    print(score_max)
    return score_max


if __name__ == '__main__':

    
    # plateau_score(20,0.4,2,0.03)

    df_list = pd.read_csv("2912_shapre_ratio.csv", index_col=0)
    index_list = list(df_list.index.values)
    column_list = list(df_list.columns)

    score_heatmap(df_list)
    # print(plateau_score(list, 3, 3, 2, 0.1))