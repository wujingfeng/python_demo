import math
import os.path
import threading

import requests
from bs4 import BeautifulSoup

host = 'https://www.nvlang.org/'
jiepai = 'new/guonei/page/'
articleRoute = 'archives/{}.html'

header = {
    "cookie": "wordpress_logged_in_d6a54ecf5252fd21adb5f20dc2c9af62=yangDrui%7C1657853837%7CIWOKSNtRVmDmrcfB6P0XKnvfbzhanNBgEin1hcFeqoj%7Cdf2ac0bf463c70d8ee5cc87f8a6e55d7e9a9eebd72a8e7fe70c27b9fa75f4aaf; Hm_lvt_a5c6f20ccb33a03f66b4f3c265b9aa31=1656644162,1657423445; Hm_lpvt_a5c6f20ccb33a03f66b4f3c265b9aa31=1657454679",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

threadsNum = 8

'''
列表解析
'''


def parseTotal():
    url = host + jiepai + str(1)
    response = requests.get(url=url, headers=header)
    if response.status_code != 200:
        print("总条数获取失败")
        return ""
    soup = BeautifulSoup(response.text)
    total = soup.select(".next-page")[0].previous_sibling.string

    print("总页数为：", total)
    for page in range(2, int(total) + 1):
        url = host + jiepai + str(page)
        parseList(url)
        print("当前采集总进度， %d/%d" % (page, int(total)))


def parseList(url):
    try:
        response = requests.get(url=url, headers=header)
        if response.status_code != 200:
            print("采集失败， url=", url)

        soup = BeautifulSoup(response.text)
        # 获取列表区域
        posts = soup.select("#posts")[0]
        # 获取所有的图片内容区域
        posts = posts.select("div[class='post grid']")
        for p in posts:
            # 获取文章 id
            articleId = p.get("data-id")
            articleUrl = (host + articleRoute).format(articleId)
            parseArticle(articleUrl)
    except:
        print("列表采集失败， url=", url)


def parseArticle(url):
    try:
        response = requests.get(url=url, headers=header)
        if response.status_code != 200:
            print("采集失败， url=", url)

        soup = BeautifulSoup(response.text)
        aList = soup.select(".fb-link,.ari-fancybox")
        articleName = soup.select(".article-title")[0].string
        # 检测地址是否存在
        filePath = './img/' + articleName + '/'
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        i = 1
        currentLoop = 1
        dataList = []
        for a in aList:
            # 图片地址
            src = a.select("img")[0].get("src")
            # savePic(filePath, src)
            dataList.append({"filePath": filePath, "src": src})
            print("当前套图《" + articleName + "》保存进度：%d/%d" % (i, len(aList)))
            i += 1
        dataList = chunkData(dataList, 20)

        for dataItem in dataList:
            threads = []
            for d in dataItem:
                threads.append(
                    threading.Thread(target=savePic, args=(d['filePath'], d['src']))
                )
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    except:
        print("详情采集失败， url=", url)


def savePic(filePath, picUrl):
    # 远程图片地址
    filename = ""
    try:
        filename = str.split(picUrl, '/')[-1]

        response = requests.get(url=picUrl).content
        with open(filePath + filename, 'wb') as f:
            f.write(response)
    except:
        print("图片下载失败， url=", picUrl)

    print("图片保存成功。", filePath, filename)


def threadCrawl(dataList):
    threads = []
    for d in dataList:
        threads.append(
            threading.Thread(target=parseArticle, args=(d,))
        )
    for t in threads:
        t.start()
    for t in threads:
        t.join()


'''
将一个大列表拆分为多个小列表
'''


def chunkData(data, chunkNum=8):
    # data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    newList = list(
        map(lambda x: data[x * chunkNum:x * chunkNum + chunkNum], list(range(0, math.ceil(len(data) / chunkNum)))))

    return newList


parseTotal()
