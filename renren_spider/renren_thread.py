# coding=utf8
import os
import re
import threading
import urllib2

from bs4 import BeautifulSoup
import time

# TODO 修改为自己的Cookie
COOKIE = 'anonymid=hp1y65b2-u4y60; _r01_=1; prf_cmd_frd=0; jebe_key=e1bda92e-34a6-43a8-9545-488b4188ae09%7C19a14b39b95662d62fd1d1c4df556f32%7C1389172287493%7C1; _de=EDF26EBE42FF267F303554EBBEB4676C696BF75400CE19CC; l4pager=0; at=1; depovince=GW; jebecookies=6114cc15-529c-48cb-b08c-39a43ea640f6|||||; JSESSIONID=abccnvO4akaTQdXtM9npu; p=1a8428f1ce076aa9a78e47248fa216234; ap=341396474; t=d4bbf4277354165b42460e31467413a24; societyguester=d4bbf4277354165b42460e31467413a24; id=341396474; xnsid=3209986e; XNESSESSIONID=fbfc8f557f64; loginfrom=null; feedType=341396474_hot'
HEADERS = {'cookie': COOKIE}

# find title     
def find_title(mypage):
    myMatch = re.search(r'<title>(.+?)</title>', mypage, re.S)
    title = u'undefined'
    if myMatch:
        title = myMatch.group(1)
    else:
        print u'find no title'
        # 文件名不能包含以下字符： \ / ： * ? " < > |
        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"',
                                                                                                                    '').replace(
            '>', '').replace('<', '').replace('|', '')
    return title

def login_renren(url):
    try:
        req = urllib2.Request(url, headers=HEADERS)
        page = urllib2.urlopen(req).read()
        page = page.decode('utf-8')
        title = find_title(page)
        print title
        return page
    except:
        page = ur''
        return page

def find_friendlist():
    url_friend = 'http://friend.renren.com/groupsdata'    #friend list
    req = urllib2.Request(url_friend, headers=HEADERS)
    try:
        page = urllib2.urlopen(req).read()
        page = page.decode('utf-8')
    except:
        print 'cookie is error'
        page = ''
    pattern = re.compile(r'"fid":\d*?,')
    if pattern.findall(page):
        list = pattern.findall(page)
        friend_file = open('../id.txt', 'w')
        for i in list:
            id = i[6:-1]
            friend_file.write(id)
            friend_file.write(os.linesep)
        friend_file.close()
    else:
        print 'find no friendID'

# http://photo.renren.com/photo/XXXXXXXXX/album/relatives/profile
# http://photo.renren.com/photo/XXXXXXXXX/album-535947620?frommyphoto
def find_ablumUrl():
    list = ur''
    file = open('../id.txt')
    ablum = open('../albumlist.txt', 'w')
    while 1:
        line = file.readline()
        if line:
            line = line[:-1]
            photo_url = 'http://photo.renren.com/photo/' + str(line) + '/album/relatives/profile'
            print photo_url
            data = login_renren(photo_url)
            pattern = re.compile(r'http://photo.renren.com/photo/(.+?)frommyphoto')
            if pattern.findall(data):
                list = pattern.findall(data)
            else:
                print 'find no album id'
                #remove duplicate album id
            albumid_set = set()
            for i in list:
                albumid_set.add(i)

            for i in albumid_set:
                album_list = 'http://photo.renren.com/photo/' + str(i) + 'frommyphoto'
                print album_list
                ablum.write(album_list)
                ablum.write(os.linesep)
        else:
            break

def download_album():
    file = open('../albumlist.txt')
    while 1:
        line = file.readline()
        if not line:
            break
        else:
            list = ''
            data = login_renren(line)
            pattern = re.compile(r'large:.*?\.jpg', re.I)   #large xlarge
            if pattern.findall(data):
                list = pattern.findall(data)
            else:
                print 'found no image'

            photo_url = set()
            for i in list:
                i = i[7:]
                photo_url.add(i)
                print i   # test
            try:
                d = Download(photo_url)
                print d.name
                d.start()
            except:
                print u'download error   ' + line
    file.close()

#download by thread
class Download(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        for i in self.que:
            try:
                data = urllib2.urlopen(i).read()
                path = savePath + str(i[-15:-5]) + '.jpg'
                f = open(path, 'wb')  # 存储下载的图片
                f.write(data)
                f.close()
            except:
                print 'download error'
        return

#start
def start_photo_grap():
    login_renren(URL)
    find_friendlist()
    find_ablumUrl()
    download_album()


URL = r'http://www.renren.com'
savePath = r'./renren1/'

if __name__ == '__main__':
    start_photo_grap()
    print 'success '