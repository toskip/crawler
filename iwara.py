from requests_html import HTMLSession
from threading import Thread
from queue import Queue
import time
def listdownload(threadnum,listqueue,contentqueue):
    while True:

        url = listqueue.get(False)
        session = HTMLSession()
        proxy_dict = {
            "http": "http://127.0.0.1:1080/",
            "https": "http://127.0.0.1:1080/"
        }
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        }
        i = url.split("=")[-1]
        r = session.get(url, proxies=proxy_dict)

        content = r.html.find(".field-items > div > a")
        for each in content:
           for link in each.absolute_links:
               contentqueue.put(link)
        print(f"线程{threadnum}: 处理完毕{i}")
        r.close()

def contentdownload(threadnum,contentqueue,f):
    while True:
        url = contentqueue.get(False)
        session = HTMLSession()
        proxy_dict = {
            "http": "http://127.0.0.1:1080/",
            "https": "http://127.0.0.1:1080/"
        }
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        }
        r = session.get(url, proxies=proxy_dict)
        json = {}
        json["content"] = r.html.find(".field-items > div > a").text()
        f.write(json)
        print(f"线程{threadnum}:")
        r.close()

if __name__ == '__main__':

    listqueue = Queue()
    contentqueue = Queue()
    for i in range(814):
        listqueue.put(f"https://ecchi.iwara.tv/videos?page={i}")
    threadnum = 4  # 随便设
    t = []
    starttime = time.time()
    print('开始下载列表页,线程数%d' % (threadnum))
    for i in range(threadnum):
        thread = Thread(target=listdownload, args=(i, listqueue,contentqueue))
        thread.start()
        t.append(thread)
        print('线程%d已启动' % (i))
    for thread in t:
        thread.join()
    print('下载列表页完成')
    endtime = time.time()
    print('用时 %f' % (endtime - starttime))
    """
    
    f = open("temp.txt","w")
    starttime = time.time()
    t2 = []
    print('开始下载内容页,线程数%d' % (threadnum))
    for i in range(threadnum):
        thread = Thread(target=contentdownload, args=(i,contentqueue,f))
        thread.start()
        t2.append(thread)
        print('线程%d已启动' % (i))
    for thread in t2:
        thread.join()
    print('下载内容页完成')
    endtime = time.time()
    print('用时 %f' % (endtime - starttime))
    f.close()
    """
