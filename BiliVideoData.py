import requests
import json
import datetime
import csv

def ReadBvidFromJson(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get('bvids', []),data.get('uid', '')

def GetVideoInfo(bvid, uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        video_info = response.json()['data']
        # Unix时间戳处理
        pubdate_timestamp = video_info['pubdate']
        pubdate_readable = datetime.datetime.fromtimestamp(pubdate_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return {
            "bvid": bvid,
            "uid": uid,
            "title": video_info['title'],
            "tname": video_info['tname'],
            "pubdate": pubdate_readable,
            "view": video_info['stat']['view'],
            "danmaku": video_info['stat']['danmaku'],
            "reply": video_info['stat']['reply'],
            "favorite": video_info['stat']['favorite'],
            "coin": video_info['stat']['coin'],
            "share": video_info['stat']['share'],
            "like": video_info['stat']['like'],
        }
    except requests.RequestException as e:  # 捕获请求相关的异常
        print(f"Error fetching info for BVID {bvid}: {e}")
        return None
    except KeyError as e:  # 捕获数据解析错误
        print(f"Key error when parsing data for BVID {bvid}: {e}")
        return None

def SaveToCSV(video_info, filename='data/VideoInfo5.csv'):
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["bvid", "uid", "title", "tname", "pubdate", "view", "danmaku", "reply", "favorite", "coin", "share", "like"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(video_info)

def SaveProblematicBvids(bvids,uid, filename='data/ProblematicBvids5.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        data = {"bvids": bvids,"uid": uid}  # 构造包含bvids关键字的字典
        json.dump(data, file, ensure_ascii=False, indent=4)

def InitializeCsvFile(fieldnames, filename='data/VideoInfo5.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if __name__ == '__main__':
    # json_path = 'data/UPData5.json'
    json_path = 'data/ProblematicBvids5.json'
    BvidList,uid = ReadBvidFromJson(json_path)
    ProblematicBvids = [] # 存储出问题的BVID

    if BvidList:
        if "ProblematicBvids" not in json_path:
            InitializeCsvFile(["bvid", "uid", "title", "tname", "pubdate", "view", "danmaku", "reply", "favorite", "coin", "share", "like"])
        for bvid in BvidList:
            video_info = GetVideoInfo(bvid,uid)
            if video_info is not None:
                SaveToCSV(video_info)
            else:
                ProblematicBvids.append(bvid)
        SaveProblematicBvids(ProblematicBvids,uid)
    else:
        print("未从JSON文件中读取到数据")