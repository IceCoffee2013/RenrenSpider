import re
import urllib
import urllib2
import time
import sys
import os

__author__ = 'Langley'
# TODO 修改为你自己的Cookie
COOKIE = 'anonymid=hncstqv4-e3vws; _r01_=1; _de=EDF26EBE42FF267F303554EBBEB4676696BF75400CE19CC; jebe_key=1d74e4d6-2b1b-4080-86d1-43d379c7c41%7C19a14b39b95662d62fd1d1c4df556f32%7C1385625216085%7C1; l4pager=0; __utma=1048322.1504170355.1386044840.1386044840.1386044840.1; __utmz=10481322.1386044840.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); depovince=JS; JSESSIONID=abcPnJRJxOp-re3XTCrlu; at=1; jebecookies=91645232-d143-4871-b682-112c109dbce7|||||; p=5a62bc91f1bc9412773726c43a53e64e4; ap=341396474; first_login_flag=1; t=81abfd17d094104d94c6e30d1929c2764; societyguester=81abfd17d094104d94c6e30d1929c2764; id=341396474; xnsid=2a3f7082; loginfrom=null; feedType=341396474_hot'
HEADERS = {'cookie': COOKIE,
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
ID = '341396474'  # TODO 修改为你的人人ID，个人主页url最后一段数字
reload(sys)
sys.setdefaultencoding('utf-8')


def login_renren(url):
    try:
        req = urllib2.Request(url, headers=HEADERS)
        page = urllib2.urlopen(req).read()
        #     page = urllib2.urlopen(url).read()
        page = page.decode('utf-8')
        # title = find_title(page)
        # print title
        return page
    except:
        page = ur''
        return page


def publish(content):
    url1 = 'http://shell.renren.com/' + ID + '/status'
    postdata = {
        'content': content,
        'hostid': ID,
        'requestToken': 851523123, #
        '_rtk': 'fe82348d', #
        'channel': 'renren',
    }
    req1 = urllib2.Request(url1, urllib.urlencode(postdata), headers=HEADERS)
    page_data = urllib2.urlopen(req1).read()
    print page_data


def more_page():
    url2 = 'http://notice.renren.com/show?uid=341396474&site=renren'
    url4 = 'http://www.renren.com/activity/get/data'
    postdata = {
        'requestToken': 851523123, #
        '_rtk': 'fe82348d', #
    }
    req = urllib2.Request(url4, urllib.urlencode(postdata), headers=HEADERS)
    page = urllib2.urlopen(req).read()
    file = open(str(time.time()) + '.html', 'w')
    file.write(page)
    file.close()


def get_chatid():
    url3 = 'http://photo.renren.com/photo/data'
    postdata = {
        'userId': 341396474,
        'requestToken': 851523123, #
        '_rtk': 'fe82348d', #
    }
    req = urllib2.Request(url3, headers=HEADERS)
    page = urllib2.urlopen(req).read()
    page = page.decode('utf-8')
    file = open(str(time.time()) + '.html', 'w')
    file.write(page)
    file.close()


def friend_list():
    url3 = 'http://photo.renren.com/photo/data'   #news
    url_friend = 'http://friend.renren.com/groupsdata'    #friend list
    req = urllib2.Request(url_friend, headers=HEADERS)
    page = urllib2.urlopen(req).read()
    page = page.decode('utf-8')
    file = open(str(time.time()) + '.html', 'w')
    file.write(page)
    file.close()
    pattern = re.compile(r'"fid":\d*?,')
    list = pattern.findall(page)
    friend_file = open('../file_list.txt', 'w')
    for i in list:
        id = i[6:-1]
        print id
        friend_file.write(id)
        friend_file.write(os.linesep)
    friend_file.close()


friend_list()
print 'success'