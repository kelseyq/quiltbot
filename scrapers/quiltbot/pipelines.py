# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy


class QuiltbotPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        return 'full/%s' % (request.meta['block_number'] + '.jpg')

    def get_media_requests(self, item, info):
        for file_url in item['image_urls']:
            yield scrapy.Request(file_url, meta={'block_number': item['block_number']})