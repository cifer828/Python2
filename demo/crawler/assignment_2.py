#encoding=utf8
from lxml import html
import urllib2
import re
from WebData.Examples.BeautifulSoup import *

PAGES = 5
books = []
base_url = "https://book.douban.com/"
url = base_url + 'tag/%E5%B0%8F%E8%AF%B4' # 豆瓣小说
next_page_xpath = "//span[@class='next']/a/@href"
title_xpath = '//li[@class="subject-item"]/div[@class="info"]/h2/a/@title'
pub_xpath = '//li[@class="subject-item"]/div[@class="info"]/div[1]/text()'
star_xpath = '//li[@class="subject-item"]/div[@class="info"]/div[2]/span[2]/text()'
pl_xpath = '//li[@class="subject-item"]/div[@class="info"]/div[2]/span[3]/text()'
# print BeautifulSoup(html_text).prettify()

def download(path, PAGES):
    """
     爬取豆瓣小说的前PAGES页的书目内容，并保存在path路径下
    """
    global url
    for i in range(PAGES):
        html_text = urllib2.urlopen(url).read()
        root = html.fromstring(html_text)
        titles = root.xpath(title_xpath)
        pubs = root.xpath(pub_xpath)
        stars = root.xpath(star_xpath)
        pls = root.xpath(pl_xpath)
        url = base_url + root.xpath(next_page_xpath)[0].encode("utf8") # 网址中存在中文需转码
        for book in zip(titles, pubs, stars, pls):
            books.append(process_item(book))
    write2file(books, path)

def write2file(books, path):
    """
    将书目信息列表book按行保存在path路径下
    """
    fhand = open(path, 'wb')
    fhand.write(u"书名\t\t作者\t\t出版社\t\t出版日期\t\t定价\t\t评星\t\t评论人数\n".encode('utf8'))
    for book in books:
        for item in book:
            # print item
            fhand.write(item.encode('utf8'))
            fhand.write('\t\t')
        fhand.write('\n')


def process_item(rawbook):
    """
    对爬取的原始书目信息进行简单处理
    """
    book = []
    for i in range(4):
        item = rawbook[i].strip()
        if i == 1:
            # 原始格式为 作者1/作者2.../出版社/出版日期/定价
            book.append(re.findall('(.*)(/[^/]*){3}$', item)[0][0].strip()) #作者
            book.append(re.findall('/([^/]*)(/[^/]*){2}$', item)[0][0].strip()) # 出版社
            book.append(re.findall('/([^/]*)/[^/]*$', item)[0].strip()) # 出版日期
            book.append(re.findall('/([^/]*)$',item)[0].strip()) # 定价
        elif i == 2:
            book.append(item + u'星') # 评星
        elif i == 3:
            # print item
            book.append(re.findall('\d+',item)[0] + u'人') # 评论人数取数字
            # print re.findall('(\d+)',item)[0]
        else:
            book.append(item) # 书名
    return book

# 文件名'豆瓣小说.txt'，爬取5页内容
download(u'豆瓣小说.txt', 5)
# open(u'豆瓣小说.txt', 'wb').write(u"书名\t作者\t出版社\t出版日期\t定价\t评星\t评论人数\n".encode('utf8'))
# print re.findall('(.*)(/[^/]*){3}$', u'(日)东野圭吾 / 李盈春 / 南海出版公司 / 2014-5 / 39.50元')[0][0]
