# 并发，  多线程实现
import threading
import time


def crawl(url):
    time.sleep(0.2)
    print(url)


def multiCrawl():

    for r in range(4):
        time.sleep(1)
        threads = []
        print("当前第", r, '次循环')
        for i in range(30):
            threads.append(
                threading.Thread(target=crawl, args=(i,))
            )
        for t in threads:
            t.start()

        for t in threads:
            t.join()


def singleCrawl():
    for i in range(30):
        crawl(i)


if __name__ == '__main__':
    startTime = time.time()
    multiCrawl()
    endTime = time.time()
    print("multiCrawl花费时间：", endTime - startTime)

    # startTime = time.time()
    # singleCrawl()
    # endTime = time.time()
    # print("singleCrawl花费时间：", endTime - startTime)