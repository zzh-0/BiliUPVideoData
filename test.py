import json
with open("UPData.json", 'r', encoding='utf-8') as file:
    data = json.load(file)
list=data.get('bvids', [])  # 默认返回空列表，如果'bvids'不存在于JSON中
print(len(list))