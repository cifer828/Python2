# -*- coding: utf-8 -*-
import scrapy
from ..items import PedailyItem
import re
import datetime
import chardet

class PedailySpider(scrapy.Spider):
    name = "pedaily"
    allowed_domains = ["pedaily.cn"]
    start_urls = [
        "http://www.pedaily.cn/all",
    ]
    def __init__(self):
        self.stop = False
        self.num = 0
        self.id = 0
        self.base_url =  "http://www.pedaily.cn/all"

    def parse(self, response):
        for href in response.xpath('//ul[@id="newslist-all"]/li/h3/a/@href').extract():
            # 跟踪链接
            yield scrapy.Request(href, callback=self.parse_contents)
        if self.stop:
            # 遇到过期新闻停止爬取
            return
        self.num += 1
        next_page_url = self.base_url + '/' + str(self.num)
        # 翻页
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_contents(self, response):
        if self.stop:
            return
        item = PedailyItem()
        self.id += 1
        item['link'] = response.url
        if response.url.startswith('http://newseed'):
            item['title'] = response.xpath('//div[@class="col-md-660"]/div/h1/text()')[0].extract().encode('utf8')
        else:
            item['title'] = response.xpath('//h1[@id="newstitle"]/text()').extract()[0].encode('utf8')
        item['id'] = self.id
        item['link'] = response.url.encode('utf8')
        # 合并段落
        p = response.xpath('//div[@id="news-content"]/p/text()').extract()
        item['content'] = ''.join(p).encode('utf8')
        item['time'] = response.xpath('//span[@class="date"]/text()').extract()[0].encode('utf8')
        self.stop = self.stop_at(item['time'])
        yield item

    def stop_at(self, date_string):
        """
        七天以内True
        七天以外False
        """
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        diff = datetime.datetime.now() - date
        print diff.days
        return diff.days > 7



