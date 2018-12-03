#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
爬取能源管理中心用电量网站
http://202.120.163.129:88
需在校内或连接同济vpn时才可使用
2017.3.17
增加发送邮件提醒功能
2017.4.16
更新3个__VIEWSTATE和1个__EVENTVALIDATION值
增加报错邮件功能
2017.6.22
网站更新，去除URL2提交参数，只用cookies
2017.7.27
增加多楼栋查询值字典
自动获取viewstate
"""
import urllib,urllib2
import chardet
import cookielib
from lxml import html
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# URL1--提交表单的url，类似登录界面
URL1 = "http://202.120.163.129:88"
# URL2--提交表单后跳转的url，类似登陆后跳转界面
URL2 = 'http://202.120.163.129:88/usedRecord.aspx'

def viewstate(paras):
    """
    从页面源码获取viewstate
    """
    req = urllib2.Request(URL1, paras)
    html_text =  unicode(urllib2.urlopen(req).read(), 'GB2312')
    root = html.fromstring(html_text)
    viewstate_xpath = '//input[@id="__VIEWSTATE"]/@value'
    return root.xpath(viewstate_xpath)[0]

def dorm_keys(builing, floor):
    """
    获取房间号在提交表单时对应的查询值
    """
    params_list = [('__VIEWSTATE', ''), ('__EVENTTARGET', 'dr_ceng'),
                   ('__EVENTARGUMENT', ''), ('__LASTFOCUS', ''), ('__VIEWSTATEGENERATOR', 'CA0B0334'),
                   ('drlouming', '7'), ('drceng',builing), ('dr_ceng', floor), ('drfangjian', '')]
    params = urllib.urlencode(params_list)
    # 获取两次提交后的viewstate
    params_list[0] = ('__VIEWSTATE', viewstate(params))
    params = urllib.urlencode(params_list)
    params_list[0] = ('__VIEWSTATE', viewstate(params))
    params = urllib.urlencode(params_list)

    req = urllib2.Request(URL1, params)
    html_text =  unicode(urllib2.urlopen(req).read(), 'GB2312')     # 中文转码
    root = html.fromstring(html_text)
    rooms_xpath = '//select[@id="drfangjian"]/option/text()'
    room_keys_xpath = '//select[@id="drfangjian"]/option/@value'
    rooms = root.xpath(rooms_xpath)     # 房间号
    room_keys = root.xpath(room_keys_xpath)     # 房间对应查询值
    room_dict = {}
    # rooms_dict = {房间号：查询值}
    for i in range(len(rooms)):
        room = re.findall('\S+', rooms[i])[0]
        room_dict[room] = room_keys[i]
    return room_dict, viewstate(params)

def elec_crawler(builing, floor, dorm_number):
    """
    模拟带cookies的网站登录/跳转
    """
    # builing_dict {楼号：[楼号查询值，（各层查询值，）]}
    builing_dict = {12: ['1275', ('1508', '1510', '1511', '1512', '1513', '1514', '1515')],
                    15: ['1538', ('1876', '1877', '1878', '1879', '1880', '1881', '1882')]}
    drceng =  builing_dict[builing][0]
    dr_ceng =  builing_dict[builing][1][floor - 1]
    # 获取房间号查询值
    dorm_dict, viewstate = dorm_keys(drceng, dr_ceng)
    # url1中下拉框内容随上一级下拉菜单变化而更新，param1仅为最后一次提交的表单，前面更新下拉菜单所提交的表单省略
    params1 = urllib.urlencode([('__EVENTTARGET', ''), ('__EVENTARGUMENT', ''), ('__LASTFOCUS', ''), ('__VIEWSTATEGENERATOR', 'CA0B0334'),
                               ('__VIEWSTATE', viewstate),
                               ('drlouming', '7'), ('drceng', drceng), ('dr_ceng', dr_ceng), ('drfangjian', dorm_dict[dorm_number]),
                               ('radio','usedR'), ('ImageButton1.x', '40'), ('ImageButton1.y', '21')])

    # url2中表单为阻止跳转回url1
    # params2 = urllib.urlencode([('__VIEWSTATEGENERATOR', '81FE99AE'), ('__VIEWSTATE', '/wEPDwUKMTA5MzUzNjU2OGRkuIVkF2XV7poJn88jH3/K2D7ROGRtCjnHJtbfiNQMtpY='),
    #                        ('__EVENTVALIDATION', '/wEdAAT5IhCANFTKXnEbMvrYZBRE0FAlDrIj7n5hu5FXeSoIm6Yp7cPvy138AI60rKnW/P2nnFfL7Vy8mnWVKUTeRozh5AwlzvU0DmV0WL+ZD4ECVn2G+apLWfpp2nSwyjYBCq4=')])

    # 获取cookieJar实例
    cj = cookielib.CookieJar()
    # cookieJar作为参数，获得一个opener的实例
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # 伪装成一个正常浏览器
    opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0')]
    # 以post的方法访问登录url1，访问之后cookieJar会自定保存cookie
    opener.open(URL1, params1).read()
    # 以带cookie的方式访问url2
    op = opener.open(URL2)
    html_text = op.read()
    room_xpath = '//h6/text()'
    remaining_sum_xpath = '//h6/span/text()'
    root = html.fromstring(html_text)
    room_text = root.xpath(room_xpath)[0]
    room = re.findall('\d+', room_text)[0]         # 房间名
    remaining_sum = root.xpath(remaining_sum_xpath)[0]     # 剩余金额
    print u'房间号:\t\t' + room
    print u'剩余金额:\t' + remaining_sum
    return room, remaining_sum

def _format_addr(s):
    """
    格式化邮件地址,使其具有发件人名字
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),
                       addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_email(to_addr, ele):
    """
    向指定邮箱发送电费提醒邮件
    """
    from_addr = 'zhqchen@126.com'
    password = 'zqc199408282116'
    # to_addr = 'zhqchen@126.com'
    smtp_server = 'smtp.126.com'

    msg = MIMEText('房间 %r 剩余电费 %s 元，请尽快充值' % (ele[0].encode(), ele[1]), 'plain', 'utf-8')
    msg['From'] = _format_addr(u'我 <%s>' % from_addr)
    msg['To'] = _format_addr(u'你<%s>' % to_addr)
    msg['Subject'] = Header(u'电费提醒', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def reminder(building, floor, dorm, email_addr, alertline):
    """
    若剩余电费少于指定金额，发送提醒邮件
    building, floor: int
    dorm: string
    """
    ele = elec_crawler(building, floor, dorm)
    if float(ele[1]) < alertline:
        send_email(email_addr, ele)

def run():
    """
    若程序出现问题，发送报错邮件
    """
    try:
        reminder(12, 4, '435', 'zhqchen@126.com', 5)
        reminder(15, 5, '539', '1259414524@qq.com', 5)
    except:
        send_email('zhqchen@126.com', ('0000','错误'))

# viewstate()
for key, value in  dorm_keys(15, 5)[0].items():
    print key, value

# run()
# reminder(12, 4, '435', 'zhqchen@126.com', 5)
