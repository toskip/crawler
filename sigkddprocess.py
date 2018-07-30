# coding: utf-8
#多进程
from urllib import request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue,cpu_count
import os
import time
import sys
def replace_invalid_filename_char(filename, replaced_char='_'):
    '''Replace the invalid characaters in the filename with specified characater.
    The default replaced characater is '_'.
    e.g. 
    C/C++ -> C_C++
    '''
    valid_filename = filename
    invalid_characaters = '\\/:*?"<>|'
    for c in invalid_characaters:
        #print 'c:', c
        valid_filename = valid_filename.replace(c, replaced_char)

    return valid_filename 
def download(processnum,q):
    while True:
        try:
            i,j,folder,name,url = q.get(True,1)
        except:
            print('进程%s已停止'%(processnum))
            break
        for k in range(3):
            try:
                page = request.urlopen(url).read()
                soup = BeautifulSoup(page,'lxml')
                link = soup.find(target="_blank")
                headers = {
                    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
                    'Referer':url,
                    'Connection': 'keep-alive'
                }
                req = request.Request('https://dl.acm.org/authorize?'+link.get('href').split('?')[1],headers =headers)
                page = request.urlopen(req).read()
                soup= BeautifulSoup(page,'lxml')
                pdf = soup.find_all('noscript')[1].p.a.get('href')
                req = request.Request(pdf)
                open(folder+'/'+replace_invalid_filename_char(name)+'.pdf','wb').write(request.urlopen(req).read())
                print("进程%s: 第%d个表格的第%d篇文章下载成功"%(processnum,i+1,j+1))
                break
            except:
                print("进程%s: 第%d个表格的第%d篇文章下载错误，重试中"%(processnum,i+1,j+1),file=sys.stderr)
if __name__=='__main__':
    '''
    解除递归限制，不加这句队列会出问题
    http://lovenight.github.io/2015/11/12/Python%20Queue%E7%9A%84RecursionError%E8%A7%A3%E5%86%B3%E5%8A%9E%E6%B3%95/ 提供解决方案
    '''
    starttime =time.time()
    sys.setrecursionlimit(1000000) 
    q = Queue()
    page = request.urlopen(r'http://www.kdd.org/kdd2017/accepted-papers').read()
    soup = BeautifulSoup(page,'lxml')
    names = soup.find_all('h4')
    tables = soup.find_all('table')
    for i in range(1):
        links = tables[i].find_all('a')
        if not os.path.exists(names[i].string): os.mkdir(names[i].string)
        for j in range(len(links)):
            q.put((i,j,names[i].string,links[j].get_text(),links[j].get('href')))
    #启动多进程
    #threadnum = cpu_count()
    threadnum = 8 #随便设
    p = []
    print('开始下载,进程数%d'%(threadnum))
    for i in range(threadnum):
        process = Process(target = download, args=(i,q,))
        process.start()
        p.append(process)
        print('进程%d已启动'%(i))
    for process in p:
        process.join()
    print('下载完成')
    endtime = time.time()
    print('用时 %f'%(endtime-starttime))
