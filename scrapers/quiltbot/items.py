# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuiltItem(scrapy.Item):
    block_number = scrapy.Field()
    names = scrapy.Field()
    image_urls = scrapy.Field()


class BARObitItem(scrapy.Item):
    full_name = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()


class TOPObitItem(scrapy.Item):
    full_name = scrapy.Field()
    title_name = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
