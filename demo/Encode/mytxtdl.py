#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
# import sys
#
# reload(sys)
# sys.setdefaultencoding('gbk')
# print sys.getdefaultencoding()

def download(url):
    headers = {
               'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate, sdch', # download unzip file
               'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
               'Cache-Control':'no-cache',
               'Connection':'keep-alive',
               'Cookie':'referrer=; __test=42aa3f9f2dc33ef81851d2ec4610b664',
               'Host':'www.ciferzh.byethost12.com',
               'Pragma':'no-cache',
               'Upgrade-Insecure-Requests':'1',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    req = urllib2.Request(url = url, headers = headers)
    filename = re.findall('[^\/]+$', url)[0]
    netfile = urllib2.urlopen(req).read()
    print netfile
    fhand = open(filename, 'wb')
    fhand.write(netfile)
    fhand.close()

download('http://www.ciferzh.byethost12.com/css/test2.txt')


# print repr(open('test2expect.txt','r').read())
# unicodeteststr = u'吴玥辉死基佬'
# print 'Unicode: ', repr(unicodeteststr)
# print 'Unicdoe -> gbk: ', repr(unicodeteststr.encode('gbk'))
# print 'Unicode -> utf8: ', repr(unicodeteststr.encode('utf8'))
# print 'Unicode -> gbk -> gbk: ', repr(unicodeteststr.encode('gbk').decode('gbk'))
# print u'吴玥辉死基佬'.encode('gbk').decode('gbk')
#
# teststr = '\u5367\u69fd\uff0ctwitter\u7ed9\u6211\u53d1\u4e86\u4e2a\u63a8\u9001\uff0c\u8fd9\u662f\u600e\u4e48\u628a\u54b1\u4fe9\u5339\u914d\u4e0a\u7684\uff0c\u6211\u90fd\u6ca1\u586b\u8d44\u6599\u554a'
# teststr2 = '吴玥辉死基佬'
# print 'utf8: ', repr(teststr2.decode('utf8'))
# s = '�'
# print repr(s)
# \x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\x01\x1d\x00\xe2\xff