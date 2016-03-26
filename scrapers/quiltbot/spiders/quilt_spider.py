import scrapy

from quiltbot.items import QuiltItem

DB_ROOT = ''

def get_start_urls():
    for block_number in range(1, 5931):
        yield "http://" + DB_ROOT + "/FMRes/FMPro?-db=search%20the%20quilt.fp5&-sortfield=block%20number&Block%20Number={0}&-format=ZFormVw.htm&-lay=Large%20Display&-max=1&-skip=0&-token=25&-find".format(block_number)


class QuiltbotSpider(scrapy.Spider):

    name = "quiltbot"
    allowed_domains = ["173.165.165.36:591"]
    start_urls = get_start_urls()

    def parse(self, response):
        item = QuiltItem()
        item['block_number'] = response.xpath('//form/table[1]/tr/td/text()').extract()[0].strip()
        item['names'] = map(unicode.strip, response.xpath('//form/table/tr/td/table/tr/td/text()').extract())
        item['image_urls'] = ['http://173.165.165.36:591/' + response.xpath('//table[2]//tr/td[3]/form/p[2]/img/@src').extract()[0]]
        yield item


