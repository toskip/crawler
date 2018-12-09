from requests_html import HTMLSession
from threading import Thread
from queue import Queue
import codecs
import time
import json
import locale
def listdownload(session,threadnum,listqueue,contentqueue):
    while not listqueue.empty():
        url = listqueue.get(True)
        proxy_dict = {
            "http": "http://127.0.0.1:1080/",
            "https": "http://127.0.0.1:1080/"
        }
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3',
        }
        i = url.split("=")[-1]
        #r = session.get(url, proxies=proxy_dict)
        r = session.get(url)
        #r.html.render()
        content = r.html.find(".node-video")
        for each in content:
            temp = []
            for link in each.find("h3.title",first=True).absolute_links:
                temp.append(link)
            temp.append("https:"+each.find("img",first=True).attrs["src"] if each.find("img",first=True) else "")
            contentqueue.put(temp)
        print(f"线程{threadnum}: 第{i}页处理完毕，共{len(content)}条视频")
        r.close()

def contentdownload(session,threadnum,contentqueue,f):
    while not contentqueue.empty():
        url,thumbnail = contentqueue.get(True)
        proxy_dict = {
            "http": "http://127.0.0.1:1080/",
            "https": "http://127.0.0.1:1080/"
        }
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3',
        }
        #r = session.get(url, proxies=proxy_dict)
        r = session.get(url)
        info = r.html.find("div.node-info", first=True)
        data = {}
        data["title"] = info.find("h1.title",first=True).text.strip().split("\n作成者:")[0]
        data["url"] = url
        data["thumbnail"] = thumbnail
        data["username"] =  info.find("a.username",first=True).text.strip().split(" 作成日:")[0]
        data["userpage"] = "https://ecchi.iwara.tv"+info.find(".username",first=True).attrs["href"].strip()
        data["userpicture"] = "https:"+info.find(".user-picture img",first=True).attrs["src"].strip()
        data["time"] = info.find(".submitted",first=True).text.strip().split("作成日:")[-1]
        data["description"] = info.find(".field-type-text-with-summary",first=True).text.strip() if info.find(".field-type-text-with-summary",first=True) else ""
        data["tags"] = info.find(".field-name-field-categories",first=True).text.strip().split('\n')
        data["like"],data["view"] = info.find(".node-views",first=True).text.strip().split(' ')
        data["comment"] = r.html.find("#comments > .title",first=True).text.strip().split(' ')[-1] if r.html.find("#comments > .title",first=True) else "0"
        data["like"] = locale.atoi(data["like"])
        data["view"] = locale.atoi(data["view"])
        data["comment"] = locale.atoi(data["comment"])

        f.write(json.dumps(data,ensure_ascii=False)+'\n')
        print(f"线程{threadnum}:视频{data['title']}处理完毕")
        r.close()

if __name__ == '__main__':
    session = HTMLSession()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    listqueue = Queue()
    contentqueue = Queue()
    for i in range(2):
        listqueue.put(f"https://ecchi.iwara.tv/videos?page={i}")
    threadnum = 6  # 随便设
    t = []
    starttime = time.time()
    print('开始下载列表页,线程数%d' % (threadnum))
    for i in range(threadnum):
        thread = Thread(target=listdownload, args=(session,i, listqueue,contentqueue))
        thread.start()
        t.append(thread)
        print('线程%d已启动' % (i))
    for thread in t:
        thread.join()
    print('下载列表页完成')
    endtime = time.time()
    print('用时 %f' % (endtime - starttime))


    f = codecs.open("temp.txt","w","utf-8")
    starttime = time.time()
    print('开始下载视频页,线程数%d' % (threadnum))
    for i in range(threadnum):
        t[i] = Thread(target=contentdownload, args=(session,i,contentqueue,f))
        t[i].start()
        print('线程%d已启动' % (i))
    for thread in t:
        thread.join()
    print('下载视频页完成')
    endtime = time.time()
    print('用时 %f' % (endtime - starttime))
    f.close()

