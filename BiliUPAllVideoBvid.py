from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import json


class GetAllVideo():
    def __init__(self,uid):
        self.BvList = []  # 存储视频Bv号
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
            data = {"bvids": self.BvList}  # 构造包含bvids关键字的字典
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


if __name__ == '__main__':
    uid = '456664753'
    GetAllVideo(uid).run()

