#coding=utf8
import sys
import urllib
import urllib2

__author__ = 'Langley'

reload(sys)
sys.setdefaultencoding('utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}

# sid = 'B11041504'
'''
stuid: student number
pwd: student passwd
'''
def login(stuid, pwd):
    url1 = 'http://vote.onepedia.cn/index.php'
    postdata = {
        'stuid': stuid,
        'pwd': pwd, #
    }
    req1 = urllib2.Request(url1, urllib.urlencode(postdata), headers=HEADERS)
    page_data = urllib2.urlopen(req1).read()
    if '您已投过票了' in page_data:
        return False
    return True

def publish(sid):
    url1 = 'http://vote.onepedia.cn/votes.php'
    postdata = {
        'sid': sid,
        'vcount[]': 20, # 要投的人ID，审查元素可获得！！
        'submit:': '确 定 投 票', #
    }
    req1 = urllib2.Request(url1, urllib.urlencode(postdata), headers=HEADERS)
    page_data = urllib2.urlopen(req1).read()
    if '投票成功' in page_data:
        print sid + ' success'
    else:
        print sid + ' fail'
    # print page_data

# publish(sid)
# print 'success'