#encoding=utf8

import requests
import json
from lxml import html

base_url = 'http://www.smzdm.com/'
items = []
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Referer':'http://www.smzdm.com/jingxuan/',
    'X-Requested-With':'XMLHttpRequest',
    'Host':'www.smzdm.com',
    'Cookie': '',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

def first_item(url):
    """
    获取第一件商品信息
    并返回第一件商品的json_url
    """
    # 获取第一页的html
    first_page = requests.get(url, headers=headers)
    root = html.fromstring(first_page.text)

    # 获取第一件商品信息
    xpaths = [
        "//li[@class='feed-row-wide']/@timesort", # timesort_xpath
        "//li[@class='feed-row-wide']/h5/a/text()", # title_xpath
        "//li[@class='feed-row-wide']/h5/a/span/text()", # price_xpath
        "//span[@class='unvoted-wrap']/span/text()", # worthy_xpath
        "//div[@class='z-feed-foot-l'][2]/a[1]/@title", # collection_xpath
        "//div[@class='z-feed-foot-l'][2]/a[2]/@title", # comment_xpath
        "//div[@class='z-feed-foot-r'][2]/span/text()", # time_xpath
        "//div[@class='z-feed-foot-r'][2]/span/a/text()" # website_xpath
    ]
    item = []
    for i in range(1, len(xpaths)):
        try:
            item.append(root.xpath(xpaths[i])[0].strip())
        except:
            continue
    items.append(item)

    # for i in item:
    #     print i

    # 返回第一件商品的json_url
    return json_url(root.xpath(xpaths[0])[0])

def json_url(timesort):
    return base_url + 'json_more?timesort=%s' % timesort

def parse_json(url):
    """
    通过某商品的json获取下一页商品信息（20件）
    并返回该页最后一件商品的json_url
    """
    json_text = requests.get(url, headers=headers).text
    # json_text_cn = json_text.decode('unicode-escape').encode('utf8')  # unicode -> 汉字
    json_obj = json.loads(json_text)
    # print json.dumps(json_obj, indent=4).decode('unicode-escape').encode('utf8')
    for j in json_obj:
        # print j['article_title'],j['article_price'], j['article_worthy'], j['article_collection'],j['article_comment'], j['article_date'],j['article_mall']
        try:
          items.append([j['article_title'], j['article_price'], unicode(j['article_worthy']),
                      u'收藏数：' + j['article_collection'], u'评论数：' + j['article_comment'],
                      j['article_date'],  j['article_mall']])
        except:
            continue

    # for item in items:
    #     for i in item:
    #         print i
    #     print
    return json_url(json_obj[-1]['timesort'])

def download_smzdm(page):
    """
    获取page页商品信息
    """
    # 获取第一件商品信息及json_url
    json_url = first_item(base_url + '/jingxuan')
    for i in range(page):
        json_url = parse_json(json_url)
    write2file('smzdm.txt')

def write2file(path):
    """
    将商品信息写入指定文件
    """
    names = [u'值得买：', u'价格：', u'值得：', u'', u'', u'更新时间：', u'优惠网站：']
    fhand = open(path, 'wb')
    for item in items:
        # print item
        for i in range(len(item)):
            # print item[i], type(item[i])
            fhand.write(names[i].encode('utf8'))
            fhand.write(item[i].encode('utf8'))
            fhand.write('\n')
        fhand.write('\n\n')

download_smzdm(5)
# print parse_json(first_item(base_url + '/jingxuan'))