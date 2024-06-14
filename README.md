# 哔哩哔哩up视频数据可视化
[TOC]

## 文件说明

```bash
|-- data    # 数据
|-- page    # 可视化网页
|-- BiliUPAllVideoBvid.py   # 爬取某位UP的全部视频BVID
|-- BiliUPData.py			# UP个人信息
|-- BiliVideoData.py		# BVID对应的视频数据
|-- BvidNotCrawl.py			# 筛选未爬取的BVID视频数据
|-- MergeCSV.py				# 合并csv
|-- visual.ipynb			# 数据可视化
|-- README.md
```

## 数据爬取

### UP主视频信息

#### 获取所有视频BVID

见 `BiliUPAllVideoBvid.py` 

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

***注：访问此API经常性报错**

## 数据可视化

> 以五位历史区UP主为例：
>
> 小约翰可汗 23947287
> 渤海小吏 504934876
> 历史调研室 519872016
> 安州牧 7481602
> 唠点历史 10698584