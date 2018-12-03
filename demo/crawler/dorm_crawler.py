#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
利用request模拟登陆
缺点：未掌握cookies用法和动态页面的js内容
"""
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
from lxml import html
import re
import time
import os.path


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'85',
    'Content-Type':'application/x-www-form-urlencoded',
    # 'Cookie':'JSESSIONID=0F28AAA1B1A4BD704F89F1E86E3F253A; UrnNovellNidpClusterMemberId=~03~0Bslo~0A~0B~14mop~09~00; yunsuo_session_verify=339bd089465f85afdfacede163eb5aa5',
    'Host':'ids.tongji.edu.cn:8443',
    'Origin':'https://ids.tongji.edu.cn:8443',
    'Referer':'https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=66&sid=0&option=credential&sid=0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

# 使用登录cookie信息
session = requests.session()
# session.cookies = cookielib.LWPCookieJar(filename='cookies')
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie 未能加载")


post_url = "https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=418&sid=10&option=credential&sid=10"
postdata = {
    'option':'credential',
    'Ecom_User_ID':'1632524',
    'Ecom_Password':'828211',
    'submit':'登录',
}
# html_text = requests.get(post_url, headers=headers)
# print html_text.text.encode('utf8')
# root = html.fromstring(html_text.text)
# xpath = '//head/meta/@url'
# print root.xpath(xpath)
login_page = session.post(post_url, data=postdata, headers=headers)
print login_page.text
# print login_page.text
# login_cookies = login_page.cookies
# test_url = 'https://ids.tongji.edu.cn:8443/nidp/app?sid=0'
# # dorm_url = 'http://myportal.tongji.edu.cn/xsfw/sys/ssxfapp/*default/index.do?gid_=QU1QMjAxNTA4MDgxODM1NDU0NjU=#/preview'
# res = session.get(test_url, headers=headers,allow_redirects=False)
# print res.status_code
# print res.text






