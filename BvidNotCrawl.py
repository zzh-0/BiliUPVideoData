import json
import pandas as pd

# 读取CSV文件
csv_file_path = 'data/data02.csv'
df = pd.read_csv(csv_file_path)

# 获取CSV中所有的bvid
bvids_to_remove = df['bvid'].tolist()

# 读取现有的JSON文件
json_file_path = 'data/UPData2.json'  
new_json_file_path = 'data/NotCrawlBvid.json' 
with open(json_file_path, 'r') as file:
    data = json.load(file)

# 删除已爬取的bvid
data['bvids'] = [bvid for bvid in data['bvids'] if bvid not in bvids_to_remove]

# 将修改后的JSON数据保存到新的文件中
with open(new_json_file_path, 'w') as file:
    json.dump(data, file, indent=4)
print("success!")