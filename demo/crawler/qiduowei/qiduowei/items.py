# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiduoweiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    register_num = scrapy.Field()
    type = scrapy.Field()
    found_date = scrapy.Field()
    busi_term = scrapy.Field()
    state = scrapy.Field()
    address = scrapy.Field()
    busi_scope = scrapy.Field()
    register_authority = scrapy.Field()


