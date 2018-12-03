# -*- coding:utf-8 -*-
import cookielib
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import html
import urllib2
import urllib

def tianyancha_re():
    """
    使用requests，未成功
    """
    headers = {
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'CheckError': 'check',
            'Host' : 'www.tianyancha.com',
            'Proxy-Connection': 'keep-alive',
            'Referer':'http://www.tianyancha.com/company/37092000',
            'Tyc-From': 'normal',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
            }
    s = requests.session()
    urls = ['http://pv.tianyancha.com/pv',
            'http://www.tianyancha.com/tongji/37092000.json',
            'http://www.tianyancha.com/expanse/getAll.json',
            'http://www.tianyancha.com/f/isfm.json',
            'http://www.tianyancha.com/stock/count.json',
            'http://www.tianyancha.com/v2/company/37092000.json']

    data =[{'url': '/company/37092000'},
           {'random': '1493125456307'},
           {'id': '37092000'},
           {'': '' ,'id': '37092000'},
           {'graphId': '37092000'}]

    result = s.get(urls[5], headers = headers)
    result = s.get(urls[0] + urllib.urlencode(data[0]))
    for url in urls:
        result = s.get(url, headers=headers)
        print result.headers
        print result.content
        print '-------------------------------------'

    # # 获取cookieJar实例
    # cj = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0')]
    # opener.open(url3).read()
    # print cj
    # # 以带cookie的方式访问url2
    # op = opener.open(url2)
    # html_text = op.read()


tianyancha_re()

def driver_open():
    """
    返回PhantomJs driver
    """
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" )
    # driver = webdriver.PhantomJS(executable_path='C:\Software\Python27\phantomjs.exe', desired_capabilities=dcap)
    driver =  webdriver.Chrome('C:\chromedriver')
    return driver

def retrieve_page(url):
    """
    返回指定url的html
    """
    driver = driver_open()
    driver.get(url)
    # time.sleep(1)
    content = driver.page_source.encode('utf-8')
    return content

def get_company_page():
    """
    输入待搜索公司名称，返回其天眼查网页链接
    """
    company_name = raw_input('搜索公司：')
    url =  "http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % urllib2.quote(company_name)
    # print retrieve_page(url)
    root = html.fromstring(retrieve_page(url))
    company_page_xpath = '//div[@class="search_right_item"][1]/div[1]/div[1]/a/@href'
    company_name_xpath = '//div[@class="search_right_item"][1]/div[1]/div[1]/a/span/em/text()'
    company_page = root.xpath(company_page_xpath)[0]
    print '公司：', root.xpath(company_name_xpath)[0]
    print '链接：', company_page
    return company_page

def get_stockholders_info():
    """
    爬取公司股东信息
    """
    url = get_company_page()
    # print retrieve_page(url)
    root = html.fromstring(retrieve_page(url))
    stockholders_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[1]/a/text()'
    ratio_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[2]/div/div/span/text()'
    finance_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[3]/div/span/text()'
    stock_infos = zip(root.xpath(stockholders_xpath), root.xpath(ratio_xpath), root.xpath(finance_xpath))
    print '股东信息'
    for item in  stock_infos:
        print item[0], item[1], item[2]

# print retrieve_page(get_company_page())