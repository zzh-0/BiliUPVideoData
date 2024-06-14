import requests
import json

def GetUserInfo(uid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()

        # 检查返回数据中的code字段
        if data.get('code') != 0: 
            print(f"API returned error code {data['code']} for UID {uid}. Error message: {data.get('message', 'No message provided.')}")
        else:
            info = data['data']
            user_info = {
                "uid": uid,
                "name": info['name'],
                "sex": info['sex'],
                "face": info['face'],
                "sign": info['sign'],
                "level": info['level'],
            }
            
            with open('data/UPData.json', 'a', encoding='utf-8') as file:
                json.dump(user_info, file, ensure_ascii=False, indent=4)
                
            print("User info saved to data/UPData.json")
    
    except requests.RequestException as e:  
        print(f"Error fetching info for UID {uid}: {e}")
    
if __name__ == '__main__':
    uid = "504934876"
    user_data = GetUserInfo(uid)