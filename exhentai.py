import requests_html
import json
import traceback
import hashlib
from multiprocessing import Process
import socket
import fake_useragent
import time
import proxies
import proxies2
import random
ua = fake_useragent.UserAgent(verify_ssl=False)
session = requests_html.HTMLSession()
pr = [proxies.proxies,proxies2.proxies,proxies2.proxies]
def run(i,num,s):
    headers = {
        'Host':'exhentai.org',
        'Cookie':'ipb_member_id=460394; ipb_pass_hash=0437c4a69539bf25fd4afd468a52cc73; igneous=eb2c558e8; sl=dm_1; sk=1mjzg47ognnh4kq1cvcdi5bemysj',
        'User-Agent':ua.random
        }
    links = []
    results = []
    f2 = open('log_%d.log' % i,'w',encoding='utf-8')

    for j in range(1300,30000):
        if j%num!=i:
            continue
        for attempt in range(20):
            try:
                r = session.get('https://exhentai.org/?page=%d' % j,headers = headers,proxies=random.choice(pr),timeout=5)
                break
            except:
                print('failed, attempt %d' % attempt)
                if attempt>=20:
                    f2.write('failed %s' % ('https://exhentai.org/?page=%d' % j))
                    f2.flush()
        links = [each.attrs['href'] for each in r.html.find('div.gl1t > a')]
        for k,link in enumerate(links):
            try:
                link = link+'?hc=1'
                f2.write('process %d page %d link %d' %(i,j,k)+'\n')
                f2.write(link+'\n')
                f2.flush()
                print('process %d page %d link %d' %(i,j,k))
                print(link)
                for attempt in range(20):
                    try:
                        r = session.get(link,headers = headers,proxies=random.choice(pr),timeout=5)
                        break
                    except:
                        print('failed, attempt %d' % attempt)
                        if attempt>=20:
                            f2.write('failed %s' % link)
                            f2.flush()
                result = {}
                result['taglist'] = {'all':[]}
                lines = r.html.find('#taglist',first=True).text.strip().split('\n')
                for line in lines:
                    if line[-1]==':':
                        tc = line[:-1].lower().replace(' ','_')
                        result['taglist'][tc] = []
                    else:
                        result['taglist'][tc].append(line)
                        result['taglist']['all'].append(line)
                result['gdc'] = r.html.find('#gdc',first=True).text.strip()
                result['gdn'] = r.html.find('#gdn',first=True).text.strip()
                result['gn'] = r.html.find('#gn',first=True).text.strip()
                result['gj'] = r.html.find('#gj',first=True).text.strip()
                lines = r.html.find('#gdd',first=True).text.strip().split('\n')
                result['gdd'] = {}
                for line in lines:
                    if line[-1]==':':
                        tc = line[:-1].lower().replace(' ','_')
                    else:
                        result['gdd'][tc] = line
                for c in ['language','length','favorited']:
                    if c in result['gdd']:
                        result['gdd'][c] = result['gdd'][c].split(' ')[0]
                result['rating_count'] = r.html.find('#rating_count',first=True).text.strip()
                result['rating_label'] = r.html.find('#rating_label',first=True).text.strip().split(' ')[-1]
                result['c1'] = []
                for each in r.html.find('.c1'):
                    temp ={}
                    temp['comment'] = getattr(each.find('.c6',first=True),'text','').strip()
                    temp['date'] = getattr(each.find('.c3',first=True),'text','').strip().split(' UTC')[0].split('Posted on ')[-1]
                    temp['user'] = getattr(each.find('.c3',first=True),'text','').strip().split(' ')[-1]
                    temp['score'] = getattr(each.find('.c5',first=True),'text','').strip().split(' ')[-1]
                    result['c1'].append(temp)
                result['url'] = link
                result['cover'] = r.html.find('#gd1 > div',first=True).attrs['style'].split(' ')[3].split(')')[0].split('(')[-1]
                result['@id'] = hashlib.md5(link.encode('utf-8','ignore')).hexdigest()
                result['@index'] = 'ex_search'
                #results.append(result)
                s.send((json.dumps(result,ensure_ascii=False)+'\n').encode('utf-8','ignore'))
                #time.sleep(1)
            except:
                try:
                    f2.write(r.html+'\n')
                    f2.write(traceback.print_exc()+'\n')
                    f2.flush()
                except:
                    pass
    f2.close()
    #f = open('results.json','w',encoding='utf-8')
    #f.write(json.dumps(results,ensure_ascii=False,indent=4)+'\n')
    #f.close()
if __name__=='__main__':
    ps = []
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 送到logstash
    s.connect(('127.0.0.1', 8888))
    num = 10
    for i in range(num) :
        p = Process(target=run, args=(i,num,s))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
