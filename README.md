# 哔哩哔哩up视频数据可视化

- [哔哩哔哩up视频数据可视化](#哔哩哔哩up视频数据可视化)
  - [文件说明](#文件说明)
  - [数据爬取](#数据爬取)
    - [UP主视频信息](#up主视频信息)
      - [获取所有视频BVID](#获取所有视频bvid)
      - [获取所有视频信息](#获取所有视频信息)
    - [UP主个人信息](#up主个人信息)
      - [其他个人信息api](#其他个人信息api)
  - [数据可视化](#数据可视化)
    - [展示](#展示)


## 文件说明

```bash
|-- data    				# 数据
    |-- UPData.json			# UP个人信息
    |-- VideoInfo.csv		# 视频信息
|-- page   					# visual.ipynb对应可视化网页
|-- page2   				# visual2.ipynb对应可视化网页2
|-- BiliUPAllVideoBvid.py   # 爬取某位UP的全部视频BVID
|-- BiliUPData.py			# UP个人信息
|-- BiliVideoData.py		# BVID对应的视频数据
|-- BvidNotCrawl.py			# 筛选未爬取的BVID视频数据
|-- MergeCSV.py				# 合并csv
|-- visual.ipynb			# 数据可视化（废案）
|-- visual2.ipynb			# 数据可视化（最终结果）
|-- README.md
```

## 数据爬取

### UP主视频信息

#### 获取所有视频BVID

见 `BiliUPAllVideoBvid.py` 

**登录问题**：登录框 时显 时不显，显示会对爬取造成影响，建议手动登录

```python
class GetAllVideo():
    def __init__(self,uid):
        self.BvList = []  # 存储视频Bv号
        self.uid = uid # 对应up的uid
        self.browser = webdriver.Chrome()
        self.url=f'https://space.bilibili.com/{uid}/video'
        self.browser.get(self.url)

    # 登录
    def login(self):
        # self.browser.find_element(By.PARTIAL_LINK_TEXT, '登录').click()
        # 手动登录
        time.sleep(20)
    
    # 获取视频Bv号
    def GetVideoUrl(self):
        ul=WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="submit-video-list"]/ul[2]'))
        lis = ul.find_elements(By.XPATH, "li")
        for li in lis:
            self.BvList.append(li.get_attribute("data-aid"))
        with open("data/UPData.json", "w+", encoding="utf-8") as f:
            data = {"bvids": self.BvList,"uid":uid}
            data = json.dumps(data, ensure_ascii=False)
            f.write(data)

    # 翻页处理
    def NextPage(self):
        total = WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="submit-video-list"]/ul[3]/span[1]'))
        number = re.findall(r"\d+", total.text)
        total = int(number[0])
        for page in range(1, total):
            try:
                self.browser.find_element(By.LINK_TEXT, '下一页').click()
                time.sleep(2)  # 等待页面加载
                self.GetVideoUrl()
            except Exception as e:
                print(f"Failed to click next page: {e}")
        return self.BvList
    
    # 执行流程
    def run(self):
        self.login()
        self.GetVideoUrl()
        self.NextPage()
        print("success!")
```

#### 获取所有视频信息

见 `BiliVideoData.py`

API：

```
https://api.bilibili.com/x/web-interface/view?bvid={bvid}
```

获取数据如下：

|   属性   |   说明   |                   备注                   |
| :------: | :------: | :--------------------------------------: |
|   bvid   |  视频id  |                                          |
|  title   | 视频标题 |                                          |
|  tname   |   类别   |                                          |
| pubdate  | 发布日期 | 请求返回的是一个Unix时间戳，需要进行转换 |
|   view   |  观看量  |                                          |
| danmaku  |  弹幕数  |                                          |
|  reply   |  评论数  |                                          |
| favorite |  收藏数  |                                          |
|   coin   |  投币数  |                                          |
|  share   |  分享数  |                                          |
|   like   |  点赞数  |                                          |

在实际获取中，因为网络问题，出现个别` BVID `对应的视频数据未获取的现象，故在 `BiliVideoData.py` 文件中添加 `SaveProblematicBvids` 函数存储出问题的 `BVID` ，此外，又补充文件 `BvidNotCrawl.py` 筛选未爬取的`BVID`

### UP主个人信息

见 `BiliUPData.py`

API：

```
https://api.bilibili.com/x/space/acc/info?mid={uid}
```

***注：访问此API经常性报错，由于数据分析未用到这些数据，所以未深入探究**

#### 其他个人信息api

获取粉丝数和关注数

```
https://api.bilibili.com/x/relation/stat?vmid={uid}
```

获取总播放量和点赞量

```
https://api.bilibili.com/x/space/upstat?mid={uid}
```



## 数据可视化

见 `visual2.ipynb`

> 以五位历史区UP主为例（截至日期：2024年6月14日）：
>
> - [小约翰可汗](https://space.bilibili.com/23947287) 23947287
>   data/UPData1.json
>   data/VideoInfo1.csv
> - [渤海小吏](https://space.bilibili.com/504934876) 504934876
>   data/UPData2.json
>   data/VideoInfo2.csv
> - [历史调研室](https://space.bilibili.com/519872016) 519872016
>   data/UPData3.json
>   data/VideoInfo3.csv
> - [安州牧](https://space.bilibili.com/7481602) 7481602
>   data/UPData4.json
>   data/VideoInfo4.csv
> - [唠点历史](https://space.bilibili.com/10698584) 10698584
>   data/UPData5.json
>   data/VideoInfo5.csv

### 展示

见 `page2` 目录

下面只展示部分可视化图表

![p1](https://cdn.jsdelivr.net/gh/zzh-0/Pic@img/img/202406262236477.png)


![p2](https://cdn.jsdelivr.net/gh/zzh-0/Pic@img/img/202406262235292.png)


![p3](https://cdn.jsdelivr.net/gh/zzh-0/Pic@img/img/202406262234646.png)


![p4](https://cdn.jsdelivr.net/gh/zzh-0/Pic@img/img/202406262234156.png)


