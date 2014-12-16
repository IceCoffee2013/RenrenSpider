#coding=utf8
import xlrd
import sys
from school_vote import vote

reload(sys)
sys.setdefaultencoding('utf-8')

fname = 'file.xls'
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("在校本科生和专科生名单")
except:
    print "no sheet in %s named Sheet1" % fname
#获取行数
nrows = sh.nrows
#获取列数
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows,ncols)
#获取第一行第一列数据
for row_num in range(10130, 10230):
    s_num = sh.cell_value(row_num, 0)
    id_num = sh.cell_value(row_num, 1)[-6:]
    try:
        flag = vote.login(s_num, id_num)
        if flag:
            vote.publish(s_num)
        else:
            print s_num + ' 已投过票'
    except:
        print 'error'
    # print s_num + ' : ' + id_num