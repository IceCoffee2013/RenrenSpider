#coding=utf8
import re
import urllib
import urllib2
import time
from bs4 import BeautifulSoup

__author__ = 'Langley'
# TODO 修改为自己Cookie
COOKIE = 'anonymid=hp1y65b2-uey60; _r01_=1; jebe_key=e1bda92e-34a6-43a8-9545-488b4188ae09%7C19a14b39b95662d62fd1d1c4df556f32%7C1386731199612%7C1; _de=EDF26EBE42FF267F303554EBBEB4676C696BF75400CE19CC; prf_cmd_frd=0; l4pager=0; depovince=GW; jebecookies=c3d7720c-043c-46ea-beb1-baf66aa90a29|||||; JSESSIONID=abcBhc-zFFlhNaOAPPQnu; p=5a62bc91f1bc9412773726c43a53e64e4; ap=341396474; t=2cdbc957ff2427614f166448d84f83994; societyguester=2cdbc957ff2427614f166448d84f83994; id=341396474; xnsid=95590ced; at=1; loginfrom=null; feedType=341396474_hot'
HEADERS = {'cookie': COOKIE,
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
}
ID = '341396474' # TODO 修改为自己的人人数字ID
TARGET_ID = set(['500298679', '344457389'])  # TODO 修改为需要回复人的数字ID
REPLY_ID = set()

class Status():
    def __init__(self):
        self.url = 'http://www.renren.com'
        self.getToken(self.getPage(self.url))

    def getToken(self, page):
        p = re.compile("get_check:'(.*)',get_check_x:'(.*)',env")
        result = p.search(page)
        self.request_token = result.group(1)
        self._RTK = result.group(2)
        print self.request_token + ' : ' + self._RTK

    def loadStatus(self):
        page = self.getPage(self.url)
        soup = BeautifulSoup(page)
        list_photo = ['2032', '701']
        for i in soup.find_all('figure'):
            if i.get('data-id') in TARGET_ID: # 注释掉此段，回复所有好友
                owner_id = i.get('data-id')
                source_id = i.get('data-source')
                if source_id not in REPLY_ID:
                    print i.get('data-stype')
                    if i.get('data-stype') in list_photo:
                        isPhoto = True
                        print 'photo'
                    else:
                        isPhoto = False
                    self.autoReply(owner_id, source_id, isPhoto)
                    print i.get('data-id') + '  ' + source_id
                else:
                    print 'replyed this status'


    def autoReply(self, owner, source, isPhoto):
        if isPhoto:
            url = 'http://page.renren.com/' + str(owner) + '/photo/reply'
            # url = 'http://comment.renren.com/comment/xoa2/create'
        else:
            url = 'http://status.renren.com/feedcommentreply.do?fin=0&ft=status&ff_id=' + str(owner)
        content = '(shafa8) ' + time.strftime('于%H时%M分%S秒') + " ~"
        postdata = {
            'c': content,  #1
            'owner': owner,  #2
            'source': source,  #3
            't': 3,  #4
            'requestToken': self.request_token,  #5
            '_rtk': self._RTK,  #6
        }
        req = urllib2.Request(url, urllib.urlencode(postdata), headers=HEADERS)
        try:
            page = urllib2.urlopen(req).read()
        except:
            print '回复error'
        REPLY_ID.add(source)

    def getPage(self, url):
        try:
            req = urllib2.Request(url, headers=HEADERS)
            page = urllib2.urlopen(req).read()
            page = page.decode('utf-8')
            return page
        except:
            page = ur''
            return page


status = Status()

while True:
    status.loadStatus()
    time.sleep(20)
    print time.strftime('%H:%M:%S')
print 'success'
