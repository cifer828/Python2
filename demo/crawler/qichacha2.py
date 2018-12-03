# -*- coding:utf-8 -*-#
from lxml import html
import requests
import re
import sys
import urllib

header={
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
'host':"www.qichacha.com",
}

cookie_dict={
        'UM_distinctid':'15b94bd28c0532-06440fce5b87b3-3e64430f-15f900-15b94bd28c14d7',
        'gr_user_id':'2564fa5c-2962-4165-a15b-aacf48f7ffd7',
        '_uab_collina':'149284914580079253543107',
        'acw_tc':'AQAAAOnY9RXMkAEAsLgiOgm41tWhL1Go',
        '_umdata':'70CF403AFFD707DF01F447BEB8F98B0A64DE1388E1FB72C22705EF3B0690146152B13D1F2132E739CD43AD3E795C914C0C36F949192B7ECFBD84BF01696FBF96',
        'PHPSESSID':'996me3inl5ipjqc8f5iq4glva2',
        'gr_session_id_9c1eb7420511f8b2':'01968266-5b16-4ae1-8344-c843b6f84132',
        'CNZZDATA1254842228':'2025307065-1492848434-%7C1493263211',
        }

basic_url="http://www.qichacha.com"

def search_company(company_name, page):
    base_url =  'http://www.qichacha.com/search_index?'
    data ={'key': company_name,
           'ajaxflag': '1',
           'index': '14',
           'p': str(page),
           '':''}
    url = base_url + urllib.urlencode(data)
    # url = 'http://www.qichacha.com/search?key=' + company_name+'&ajaxflag=1&index=14&'
    print 'retrieving: ' + url
    r = requests.get(url, headers=header, cookies=cookie_dict)
    return r.content.decode('utf8')

def get_info(company_name):
    result = search_company(company_name, 1)
    root = html.fromstring(result)
    company_num_xpath = '//span[@class="text-danger"]/text()'
    company_num = int(root.xpath(company_num_xpath)[0])
    pages =  (company_num - 1) / 10 + 1
    company_list = parse_one_page(result)
    if pages > 1:
        for i in range(2, pages + 1):
            company_list += parse_one_page(search_company(company_name, i))
    for c in company_list:
        print c[0], c[1]

def parse_one_page(content):
    root = html.fromstring(content)
    name_xpath = '//tbody/tr/td[2]/a/text()'
    reg_fund_xpath = '//tbody/tr/td[3]/text()'
    name = root.xpath(name_xpath)
    reg_fund_str = root.xpath(reg_fund_xpath)
    companies = []
    for item in zip(name, reg_fund_str):
        res_fund_num = int(re.findall('(\d+)',item[1])[0])
        if res_fund_num >= 1000 and res_fund_num <= 5000:
            companies.append([item[0], res_fund_num])
    return companies

# get_info('深圳市同创伟业创业投资有限公司')
