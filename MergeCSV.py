import pandas as pd

df1 = pd.read_csv('v01.csv')
df2 = pd.read_csv('video_info.csv')

merged_df = pd.concat([df1, df2], ignore_index=True)

merged_df.to_csv('merged_file.csv', index=False)

print("合并完成！")