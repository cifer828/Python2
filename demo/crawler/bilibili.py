#encoding=utf8
"""
爬B站弹幕
1.从网页源代码找到视频弹幕的cid->2.用cid生成弹幕的xml存储地址->3.获取弹幕xml->4.提取时间、内容等
av7001393 【天天素材库】第28期
"""
import requests
import re
from lxml import etree
import time
from lxml import html

base_url = 'http://www.bilibili.com/video/'

def video_info(av_number):
    """
    获取视频名称，UP主名称
    """
    url = base_url + 'av' + av_number
    html_text = requests.get(url).text
    root = html.fromstring(html_text)
    title_xpath = "//div[@class ='v-title']/h1/text()"
    author_xpath = "//div[@class ='usname']/a/text()"
    try:
        title = root.xpath(title_xpath)[0].encode('utf8')
        author = root.xpath(author_xpath)[0].encode('utf8')
    except:
        return False
    return title,author

def bilibili_danmu(av_number):
    try:
        title,author = video_info(av_number)
    except:
        print '请输入正确的av号'
        return
    url = base_url + 'av' + av_number
    html_text = requests.get(url).text
    # 获取弹幕的cid
    cid = re.findall('cid=(\d+)', html_text)[0]
    # 生成弹幕xml
    danmu_url = 'http://comment.bilibili.com/%s.xml' % cid
    danmu_xml = requests.get(danmu_url).text
    root = etree.fromstring(danmu_xml.encode('utf8'))

    danmu = []
    dm_lst = root.findall('d')
    for item in dm_lst:
        time = danmu_time(item.get('p'))
        danmu.append([time[0],time[1],item.text])
    # 保存
    write2file( 'av' + av_number + '.txt', title, author, danmu)

def danmu_time(time_inf):
    """
    获取弹幕的出现时间和发送时间
    """
    seg = time_inf.split(',')
    time_pos = [int(float(seg[0]) / 60), int(float(seg[0]) % 60)]
    time_stamp = float(seg[4])
    time_array = time.localtime(time_stamp)
    style_time = time.strftime("%m-%d %H:%M:%S", time_array)
    return str(time_pos[0]).zfill(2) + ':' + str(time_pos[1]).zfill(2), style_time

def write2file(filename, title, author, danmu_lst):
    fhand = open(filename, 'w')
    fhand.write(title + '\n')
    fhand.write('up主: ' + author + '\n')
    fhand.write('时间\t发送日期\t\t弹幕内容\n')
    for d in danmu_lst:
        for item in d:
            try:
                 fhand.write(item.encode('utf-8') + '\t')
            except:
                continue
        fhand.write('\n')
    fhand.close()

def run():
    while 1:
        av_number = raw_input("input the av number:")
        bilibili_danmu(av_number)
        print '弹幕成功保存至' + 'av' + av_number + '.txt'

run()

