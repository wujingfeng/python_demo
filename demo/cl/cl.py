import os.path
import queue
import threading
import time

import requests
from bs4 import BeautifulSoup

paramQueue = queue.Queue()


def getContent(tid=1, like=1):
    url = "https://cl.2093x.xyz/read.php?tid=" + str(tid) + "" + "&toread=2"
    response = requests.get(url=url)
    if response.status_code != 200:
        return "文章 id 为：" + str(tid) + "的采集失败。"
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    conttpc = soup.select("#conttpc")
    contents = conttpc[0].contents
    title = soup.title.string
    articleClass = "default"
    filename = str(tid)
    if title:
        try:
            title = str.split(title, "-")[0]
            articleClass = str.split(title, ']')[0]
            articleClass = str.strip(articleClass, '[')
            filename = str.split(title, ']')[1]
        except Exception as e:
            print("tid=", tid, 'exception=', e)


    filename = filename + "-like--" + str(like)
    path = './resource/' + articleClass
    if not os.path.exists(path):
        os.makedirs(path)

    fullPath = path + '/' + filename + ".txt"
    wordCount = 0
    with open(fullPath, 'w') as f:
        f.write('\r\n' * 2)
        for content in contents:
            if content.string == None:
                f.write('\r\n')
            else:
                tmpStr = str.strip(content.string)
                wordCount += len(tmpStr)
                f.write(tmpStr)
                f.write('\r\n')

        f.seek(0, 0)
        f.write("{}, 当前文字总字数为： {}".format(title, wordCount))
        f.write('\r\n' * 2)

    newFilename = filename + "-words-" + str(wordCount)
    newFilePath = path + '/' + newFilename + ".txt"
    os.replace(fullPath, newFilePath)


def getArticleList(page=1):
    url = "https://cl.2093x.xyz/thread0806.php?fid=20&search=&page=" + str(page)
    response = requests.get(url=url)
    if response.status_code != 200:
        print("文章采集失败，" + response.text)
        return "文章采集失败，"
    soup = BeautifulSoup(response.text)
    normalTopic = soup.select("#tbody")[0]
    normalArticleList = normalTopic.select("tr")
    i = 1
    total = len(normalArticleList)
    articleId = 0
    like = 0
    for tr in normalArticleList:
        try:
            articleUrl = tr.select('td')[1].contents[1].select('a')[0]['href']
            articleId = str.split(str.split(articleUrl, '/')[-1], '.')[0]
            like = str.strip(tr.select('td')[3].text)
            getContent(int(articleId), int(like))
            # paramQueue.put({'articleId': int(articleId), 'like': int(like)})
        except BaseException as e:
            print(e)
        print("当前页数： %d,当前进度%d/%d， 当前文章 id： %s" % (page, i, total, articleId))
        i = i + 1
    print("采集完成， 当前页：", page)

    # threads = []
    # threadsNum = 8
    # for t in range(threadsNum):
    #     t = threading.Thread(target=threadArticle, args=(paramQueue,))
    #     threads.append(t)
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()


def threadArticle(threadsList):
    while True:

        try:
            param = paramQueue.get_nowait()
            i = paramQueue.qsize()
        except Exception as e:
            print(e)
            break
        getContent(param['articleId'], param['like'])


def article():
    url = "https://cl.2093x.xyz/thread0806.php?fid=20&search=&page=1"
    response = requests.get(url=url)
    if response.status_code != 200:
        print("文章采集失败，" + response.text)
        return "文章采集失败，"
    soup = BeautifulSoup(response.text)
    # 最后一页的链接，
    maxPageUrl = soup.select("#last")[2]['href']
    # 截取出最大页数
    maxPage = str.split(maxPageUrl, 'page=')[-1]
    maxPage = int(maxPage)

    for i in range(9, maxPage + 1):
        # print(i)
        getArticleList(i)
        print("当前进度：%d/%d" % (i, maxPage))


# getContent(5151936)

# 当前进度。 当前页数： 8,当前进度6/100， 当前文章 id： 4828691
article()
