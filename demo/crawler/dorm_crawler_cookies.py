# -*- coding: utf-8 -*-
"""
利用cookielib获取登录可爬页面
"""
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'option':'credential',
    'Ecom_User_ID':'1632524',
    'Ecom_Password':'828211',
    'submit':'登录',
        })
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = [
    ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    ('Accept-Encoding','gzip, deflate'),
    ('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6'),
    ('Cache-Control','max-age=0'),
    ('Connection','keep-alive'),
    ('Content-Length','85'),
    ('Content-Type','application/x-www-form-urlencoded'),
    # 'Cookie':'JSESSIONID=0F28AAA1B1A4BD704F89F1E86E3F253A; UrnNovellNidpClusterMemberId=~03~0Bslo~0A~0B~14mop~09~00; yunsuo_session_verify=339bd089465f85afdfacede163eb5aa5',
    ('Host','ids.tongji.edu.cn:8443'),
    ('Origin','https://ids.tongji.edu.cn:8443'),
    ('Referer','https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=66&sid=0&option=credential&sid=0'),
    ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
]
opener.addheaders=headers
# 登录同济身份验证系统的URL
loginUrl = 'https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=66&sid=0&option=credential&sid=0'
# 模拟登录，并把cookie保存到变量
result = opener.open(loginUrl,postdata)
# 保存cookie到cookie.txt中
cookie.save(ignore_discard=True, ignore_expires=True)
# 利用cookie请求访问另一个网址，此网址是成绩查询网址
gradeUrl = 'http://myportal.tongji.edu.cn/xsfw/sys/ssxfapp/*default/index.do?gid_=QU1QMjAxNTA4MDgxODM1NDU0NjU=#/preview'
# 请求访问成绩查询网址
result = opener.open(gradeUrl)
print result.read()