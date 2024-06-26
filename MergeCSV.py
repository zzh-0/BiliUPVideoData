import pandas as pd

# 初始化一个空列表来保存数据框
dataframes = []

# 循环遍历从1到5（包括5），构造文件名并读取数据
for i in range(1, 6):
    filename = f'data/VideoInfo{i}.csv'
    df = pd.read_csv(filename)
    dataframes.append(df)

# 合并所有数据框
merged_df = pd.concat(dataframes, ignore_index=True)

# 保存到新的CSV文件
merged_df.to_csv('data/AllVideoInfo.csv', index=False)
