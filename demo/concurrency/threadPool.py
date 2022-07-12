import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def test1(url):
    print("test", int(time.time()), url)
    time.sleep(0.2)


time1 = time.time()
executor = ThreadPoolExecutor(max_workers=20)
futures_tasks = [executor.submit(test1, url) for url in range(100)]
wait(futures_tasks, return_when=ALL_COMPLETED)

time2 = time.time()
print("耗时：", time2 - time1)
