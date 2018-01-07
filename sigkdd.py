#encoding:utf-8
from urllib import request
from bs4 import BeautifulSoup
import os
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
page = request.urlopen(r'http://www.kdd.org/kdd2017/accepted-papers').read()
soup = BeautifulSoup(page,'lxml')
names = soup.find_all('h4')
tables = soup.find_all('table')
for i in range(4):
    links = tables[i].find_all('a')
    if not (os.path.exists(names[i].string)): os.mkdir(names[i].string)
    for j in range(len(links)):
        page = request.urlopen(links[j].get('href')).read()
        soup = BeautifulSoup(page,'lxml')
        link = soup.find(target="_blank")
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer':links[j],
            'Connection': 'keep-alive'
        }
        req = request.Request('https://dl.acm.org/authorize?'+link.get('href').split('?')[1],headers =headers)
        page = request.urlopen(req).read()
        soup= BeautifulSoup(page,'lxml')
        pdf = soup.find_all('noscript')[1].p.a.get('href')
        req = request.Request(pdf)
        open(names[i].string+'/'+replace_invalid_filename_char(links[j].get_text())+'.pdf','wb').write(request.urlopen(req).read())
        print("正在下载第%d个表格的第%d篇文章"%(i+1,j+1))
