import requests
from bs4 import BeautifulSoup
import myconfig
import time
import pymysql
import multiprocessing
import redis
import random
import pymongo as mo
import re
import threading
import sys


class qsbk():
    '''糗事百科段子爬虫，爬取用户id放入redis，读取id并将用户信息及笑话保存至mongodb'''

    # 使用阿布云代理访问
    def proxy(self):  # 获取代理

        if random.random() < 0:
            conn = pymysql.connect(myconfig.host, myconfig.user, myconfig.passwd, myconfig.DB_NAME)
            cursor = conn.cursor()
            cursor.execute('select * from ipproxy.httpbin;')
            # pro=cursor.fetchone()
            count_all = cursor.fetchall()
            cursor.close()
            conn.close()
            ip = random.choice(count_all)
            ip = ip[1] + ':' + str(ip[2])
            proxies = {"http": "http://" + ip, "https": "https://" + ip}
        else:
            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"

            # 代理隧道验证信息
            dd = random.random()
            # if dd < 0.333:
            #     proxyUser = "H8X7661D3289V75D"
            #     proxyPass = "C5EC2166093B3548"
            # elif dd < 0.6666:
            #     proxyUser = "H746QK9967YC612D"
            #     proxyPass = "541E8B324C476D54"
            # else:
            #     proxyUser = "H184S812T5JOWA3D"
            #     proxyPass = "04410CA8089EF4CC"

            proxyUser = "H887SMOL77Q0848D"
            proxyPass = "FD75684EF149F5D1"

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
                "user": proxyUser,
                "pass": proxyPass,
            }

            proxies = {
                "http": proxyMeta,
                "https": proxyMeta,
            }
        return proxies

    # 读取页面，所有页面都在这里读取
    def getBSurl(self, url):
        # proxy = '115.202.190.177:9020'
        # proxies = {"http": "http://" + proxy,
        #            "https": "https://" + proxy}
        kk = 1
        while True:
            try:
                r2 = requests.get(url, headers=myconfig.headers(), proxies=self.proxy(), timeout=myconfig.timeout)  #
                rc2 = BeautifulSoup(r2.content, 'lxml')
                if rc2.text.find('糗事百科验证服务') > 0:
                    print('这个ip被封了')
                else:
                    break
            except Exception as e:
                print('qqqqqqqq{}qqqqqqqq'.format(repr(e)))
                time.sleep(0.1)
            kk = kk + 1
            if kk == 100:
                print(url)
                print('连接好多次都连不上')
                sys.exit(1)
        return rc2

    # 此人页面个数
    def article_page(self, rc2):
        aa = rc2.select('ul[class="user-navcnt"]')[0].select('a')[-2].text
        return int(aa)

    # 获取人物属性
    def people_attre(self, rc2):
        rc3 = rc2.select('div[class="user-statis user-block"]')
        try:
            pic = rc2.select('div[class="user-header"]')[0].select('img')[0].attrs['src']
        except:
            print(rc2)
        name = rc2.select_one('div[class="user-header-cover"]').text.strip('\n')
        content1 = rc3[0]
        funs_num = content1.select('li')[0].text.split(':')[1]
        atten_num = content1.select('li')[1].text.split(':')[1]
        qiushi_num = content1.select('li')[2].text.split(':')[1]
        comment_num = content1.select('li')[3].text.split(':')[1]
        face_num = content1.select('li')[4].text.split(':')[1]
        choice_num = content1.select('li')[5].text.split(':')[1]
        content2 = rc3[1]
        marri = content2.select('li')[0].text.split(':')[1]
        horoscope = content2.select('li')[1].text.split(':')[1]
        job = content2.select('li')[2].text.split(':')[1]
        hometown = content2.select('li')[3].text.split(':')[1]
        total_time = content2.select('li')[4].text.split(':')[1]
        people_att = {'name': name, 'pic': pic, 'funs_num': funs_num, 'atten_num': atten_num, 'qiushi_num': qiushi_num,
                      'comment_num': comment_num, 'face_num': face_num, 'choice_num': choice_num, 'marri': marri,
                      'horoscope': horoscope, 'job': job, 'hometown': hometown, 'total_time': total_time}
        return people_att

    # 获取糗事内容及地址
    def article_site(self, rc2):
        aa = rc2.find_all(id=re.compile('article'))
        bodyout = {}
        for a in aa:
            try:
                pic = a.find(src=re.compile('//pic')).attrs['src']
            except:
                pic = 0
            site = a.select_one('li[class="user-article-text"] > a').get('href').split('/')[2]  # 网址
            body = a.select_one('li[class="user-article-text"] > a').text.strip('\n')  # 内容
            bb = re.findall(r"\d+\.?\d*", a.select_one('li[class="user-article-stat"]').text)  # 评论
            smile = bb[0]
            comment = bb[1]
            date = bb[2] + bb[3] + bb[4]
            bodyout[site] = {'smile': smile, 'comment': comment, 'date': date, 'body': body, 'pic': pic}
            # bodyout.append([site, smile, comment, date, body])
        return bodyout

    # 获取文章评论的人并保存至redis
    def get_people(self, rc2):
        aa = [x.find(href=re.compile("/users/")).get('href').split('/')[2] for x in
              rc2.select('li[class="user-article-vote"]')]
        for a in aa:
            self.save_red(a)

    # 获取随机历史段子的人加入redis
    def addpeople(self):
        url = 'https://www.qiushibaike.com/history/'
        rc2 = self.getBSurl(url)
        for a in rc2.select('a[href*="/users/"]'):
            b = a.get('href').strip('/').split('/')[1]
            try:
                int(b)
                if len(b) == 7 or len(b) == 8 or len(b) == 6:
                    self.save_red(b)
            except:
                pass

    # 获取关注人写入redis
    def get_follows(self, begin_people):
        # return
        url = 'https://www.qiushibaike.com/users/' + begin_people + '/follows/'
        rc2 = self.getBSurl(url)
        for a in rc2.select('a[href*="/users/"]'):
            b = a.get('href').strip('/').split('/')[1]
            try:
                int(b)
                if len(b) == 7 or len(b) == 8:
                    self.save_red(b)
            except:
                pass

    # 将筛选到的人保存至redis
    def save_red(self, a):
        return
        try:
            red0 = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
            red1 = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
            if red0.keys(a) == [] and red1.keys(a) == []:
                red0.lpush(a, 0)
                print('给库新加了一个')
                # return aa
        except Exception as e:
            print(repr(e))
            print("Redis Connect Error!")
            sys.exit(1)

    # 将爬到的人所有内容保存至mongodb
    def save_mo(self, savedata):
        try:
            client = mo.MongoClient('localhost', 27017)
            databases_name = 'qsbk2'
            tablename = 'qsbk2'
            db = client[databases_name][tablename]
            db.save(savedata)
            client.close()
        except Exception as e:
            print(repr(e))
            print("Mongodb Connect Error!")
            sys.exit(1)

    # 获取时间
    def get_time(self, start, end):
        a = float(format(end - start, '0.2f'))
        return a

    # 开始的人
    def begin_people(self):
        red0 = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        yield red0.randomkey().decode()

    # 主循环
    def get_all(self, begin_people):
        url = 'https://www.qiushibaike.com/users/' + begin_people + '/articles/'
        # print(url)
        rc2 = self.getBSurl(url)
        self.get_follows(begin_people)
        try:
            if '当前用户已关闭糗百个人动态' in rc2.select_one('div[class="user-block user-setting clearfix"]').text:
                people_att = {}
                peopname = rc2.select_one('div[class="user-header-cover"]').text.strip('\n')
                people_att['flag'] = 2
                people_att['_id'] = begin_people
                people_att['name'] = peopname
                return 1
        except:
            pass
        try:
            rc2.select_one('div[class="user-header-cover"]').text.strip('\n')
        except:
            print('{}这个人空间没了'.format(url))
            print(rc2)
            return 1
        people_att = self.people_attre(rc2)  # 个人属性
        people_att['_id'] = begin_people
        if rc2.select_one('div[class="user-block user-article"]') == None:
            people_att['flag'] = 1  # 这个人没有糗事
            print('{}这个糗事少'.format(url))
            self.save_mo(people_att)
            return 1
        qs = self.article_site(rc2)  # 第一页的段子
        self.get_people(rc2)  # 把评论的人加入列表
        allpage = self.article_page(rc2)
        pageout = 1
        for i in range(allpage - 1):  # 从第二页开始
            page = i + 2
            pageout = pageout + 1
            url = 'https://www.qiushibaike.com/users/' + begin_people + '/articles/page/' + str(page) + '/'
            rc2 = self.getBSurl(url)
            qs = dict(qs, **self.article_site(rc2))
            if len(self.article_site(rc2)) < 1:
                break
            # print(page)
            # print(len(article_site(rc2)))
            self.get_people(rc2)
        people_att['flag'] = 1
        self.save_mo(dict(people_att, **qs))
        print('{}成功保存{}个页面'.format(url, pageout))
        return 1


# 多进程入口
def mulpro(peop):
    q = qsbk()
    while True:
        peop = next(q.begin_people())
        if q.get_all(peop) == 1:
            red0.move(peop, 1)
            if random.random() < 0.1:
                q.addpeople()
        else:
            pass


# 多线程入口
def multhread(n):
    threads = []
    q = qsbk()
    for t in range(n):
        threads.append(threading.Thread(target=mulpro, args=(next(q.begin_people()),)))
    for t in threads:
        # t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    crqsbk = qsbk()
    crqsbk.addpeople()
    red0 = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    flag = 1  # 1：单进程单线程；2：多进程；3：多线程；4：多进程多线程
    if flag == 1:  # 单进程单线程
        while True:
            peop = next(crqsbk.begin_people())
            if crqsbk.get_all(peop) == 1:
                red0.move(peop, 1)
                if random.random() < 0.000001:
                    crqsbk.addpeople()
            else:
                pass
                # red0.lpush('manlist', begin_people)
                # begin_people = begin_people()
                # time.sleep(2)
    elif flag == 2:  # 多进程
        numList = []
        for i in range(12):
            p = multiprocessing.Process(target=mulpro, args=(next(crqsbk.begin_people()),))
            numList.append(p)
            p.start()
    elif flag == 3:  # 多线程
        threads = []
        for t in range(8):
            threads.append(threading.Thread(target=mulpro, args=(next(crqsbk.begin_people()),)))
        for t in threads:
            # t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
    elif flag == 4:  # 多进程多线程
        numList = []
        for i in range(8):
            p = multiprocessing.Process(target=multhread, args=(2,))
            numList.append(p)
            p.start()
    print('finish')
