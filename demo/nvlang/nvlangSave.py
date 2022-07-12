import math
import os.path
import threading
import time

import requests
import re
from bs4 import BeautifulSoup

from demo.nvlang.data.articleListData import articleListData
from demo.nvlang.data.pageListData import pageListData
from demo.nvlang.data.picListData import picListData


host = 'https://www.nvlang.org/'
jiepai = 'new/guonei/page/'
articleRoute = 'archives/{}.html'

header = {
    "cookie": "wordpress_logged_in_d6a54ecf5252fd21adb5f20dc2c9af62=yangDrui%7C1657853837%7CIWOKSNtRVmDmrcfB6P0XKnvfbzhanNBgEin1hcFeqoj%7Cdf2ac0bf463c70d8ee5cc87f8a6e55d7e9a9eebd72a8e7fe70c27b9fa75f4aaf; Hm_lvt_a5c6f20ccb33a03f66b4f3c265b9aa31=1656644162,1657423445; Hm_lpvt_a5c6f20ccb33a03f66b4f3c265b9aa31=1657454679",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

threadsNum = 8
# 网站来源
site_source_nvlang = 1

# 采集状态
status_not_crawl = 1
status_crawling = 2
status_crawl_finished = 2

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
    pageData = pageListData()

    for page in range(1, int(total) + 1):
        url = host + jiepai + str(page)
        # parseList(url)
        exists = pageData.info('guonei', page)
        if not exists:
            # 不存在才插入
            res = pageData.save(page, url, 'guonei')
        print("当前采集总进度， %d/%d" % (page, int(total)))
    print("采集完成， success")


def parseList(cate='guonei'):
    pageData = pageListData()
    pageInfo = pageData.getOneUnCrawlUrlByCate(cate)
    # 修改状态为采集中
    pageData.updateStatusById(pageInfo[0], status_crawling)

    articleData = articleListData()
    while pageInfo:
        url = ""
        dataList = []
        insertData = []
        try:
            url = pageInfo[2]
            response = requests.get(url=url, headers=header)
            if response.status_code != 200:
                print("采集失败， url=", url)

            soup = BeautifulSoup(response.text)
            # 获取列表区域
            posts = soup.select("#posts")[0]
            # 获取所有的图片内容区域
            posts = posts.select("div[class='post grid']")
            i = 1
            for p in posts:
                # 获取文章 id
                articleId = p.get("data-id")
                articleName = p.select("div[class='img']>a")[0].get("title")
                articleUrl = (host + articleRoute).format(articleId)
                # parseArticle(articleUrl)
                # res = articleData.saveArticle(pageInfo[0], int(articleId), articleUrl, articleName, len(posts))
                # dataList.append({
                #     'pageId': pageInfo[0],
                #     'articleId': int(articleId),
                #     'articleUrl': articleUrl,
                #     'articleName': articleName,
                #     'total': len(posts)
                # })
                total = re.search('\[([0-9]+)P\]', articleName).group(1)
                insertData.append([
                    pageInfo[0],
                    site_source_nvlang,
                    int(articleId),
                    articleUrl,
                    articleName,
                    total,
                    int(time.time())
                ])
                print("当前分页page=%d,保存进度：%d/%d" % (pageInfo[0], i, len(posts)))
                i += 1
            articleData.batchSave(insertData)

            # dataList = chunkData(dataList, 10)
            #
            # for dataItem in dataList:
            #     threads = []
            #     for d in dataItem:
            #         threads.append(
            #             threading.Thread(target=articleData.saveArticle,
            #                              args=(
            #                                  d['pageId'],
            #                                  d['articleId'],
            #                                  d['articleUrl'],
            #                                  d['articleName'],
            #                                  d['total']
            #                              ))
            #         )
            #     for t in threads:
            #         t.start()
            #     for t in threads:
            #         t.join()
        except Exception as e:
            print("列表采集失败， url=", url, e)
            # 改为采集未完成
            pageData.updateStatusById(pageInfo[0], status_not_crawl)
        else:
            # 改为采集完成
            pageData.updateStatusById(pageInfo[0], status_crawl_finished)
            print("列表采集完成，page=%d, url=%s" % (pageInfo[0], url))
        pageInfo = pageData.getOneUnCrawlUrlByCate(cate)


def parseArticle():
    articleData = articleListData()
    articleInfo = articleData.getOneUnCrawlUrlBySource()
    articleData.updateStatusById(articleInfo[0], status_crawling)

    picData = picListData()
    while articleInfo:
        url = ""
        try:
            url = articleInfo[4]
            print("当前采集文章：url=", url)
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
            dataList = []
            insertData = []
            for a in aList:
                # 图片地址
                src = a.select("img")[0].get("src")
                # savePic(filePath, src)
                # picData.savePic(articleInfo[0], src, filePath)
                # dataList.append({"articleId": articleInfo[0], "src": src, 'filePath': filePath})
                insertData.append([
                    articleInfo[0], src, filePath, int(time.time())
                ])
                # picData.save(articleInfo[0], src)
                print("当前套图《" + articleName + "》保存进度：%d/%d" % (i, len(aList)))
                i += 1
            res = picData.batchSave(insertData)
            print(res)
            # dataList = chunkData(dataList, 10)
            #
            # for dataItem in dataList:
            #     threads = []
            #     for d in dataItem:
            #         threads.append(
            #             threading.Thread(target=picData.savePic,
            #                              args=(d['articleId'], d['src'], d['filePath']))
            #         )
            #     for t in threads:
            #         t.start()
            #     for t in threads:
            #         t.join()
        except Exception as e:
            print(e)
            print("详情采集失败， url=", url)
            articleData.updateStatusById(articleInfo[0], status_not_crawl)
        else:
            # 采集完成修改状态
            articleData.updateStatusById(articleInfo[0], status_crawl_finished)
        articleInfo = articleData.getOneUnCrawlUrlBySource()


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


# parseTotal()
# parseList()
parseArticle()

# t1 = threading.Thread(target=parseList)
# t2 = threading.Thread(target=parseArticle)
# t3 = threading.Thread(target=parseArticle)
# t4 = threading.Thread(target=parseArticle)
# # t1.start()
# t2.start()
# t3.start()
# t4.start()
