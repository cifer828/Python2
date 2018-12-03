# -*- coding:utf-8 -*-
"""
author：cifer zhang
2017.4.10
selenium + phantomjs爬取天眼查网站指定公司股东信息
"""
from selenium import webdriver
import time
from BeautifulSoup import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import html
import urllib2
import chardet

def driver_open():
    """
    返回PhantomJs driver
    """
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0" )
    driver = webdriver.PhantomJS(executable_path='C:\Software\Python27\phantomjs.exe', desired_capabilities=dcap)
    return driver

def retrieve_page(url):
    """
    返回指定url的html
    """
    driver = driver_open()
    driver.get(url)
    time.sleep(2)   # 等待
    content = driver.page_source.encode('utf-8')    # 防中文乱码
    # print content
    return content

def get_company_page():
    """
    输入待搜索公司名称，返回其天眼查网页链接
    """
    company_name = raw_input('搜索公司：')
    url =  "http://www.tianyancha.com/search?key=%s&checkFrom=searchBox" % urllib2.quote(company_name)
    print url
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
    detail_page = retrieve_page(url)
    print detail_page
    root = html.fromstring(detail_page)
    stockholders_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[1]/a/text()'
    ratio_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[2]/div/div/span/text()'
    finance_xpath = '//table[@class = "table companyInfo-table"][1]/tbody/tr/td[3]/div/span/text()'
    stock_infos = zip(root.xpath(stockholders_xpath), root.xpath(ratio_xpath), root.xpath(finance_xpath))
    print '股东信息'
    for item in  stock_infos:
        print item[0], item[1], item[2]

get_stockholders_info()