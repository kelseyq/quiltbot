import scrapy

from quiltbot.items import BARObitItem

class BARSpider(scrapy.Spider):
    name = "bar"

    def start_requests(self):
        return [scrapy.FormRequest("http://obit.glbthistory.org/olo/datesearch.jsp",
                                   formdata={'monthfrom': '01', 'yearfrom': '1972',
                                         'monthto': '12', 'yearto': '2016'},
                                   callback=self.get_obits)]

    def get_obits(self, response):
        for obit in response.xpath('//table//table//table/tr'):
            item = BARObitItem()
            item['link'] = "http://obit.glbthistory.org/olo/" + obit.xpath('td/a/@href').extract()[0]
            item['full_name'] = obit.xpath('td/a/text()').extract()[0]
            item['date'] = obit.xpath('td[2]/text()').extract()[0] + ' ' + obit.xpath('td[3]/text()').extract()[0]
            yield item