import scrapy

from quiltbot.items import TOPObitItem


def get_start_urls():
    for year in range(1982, 2016):
        yield "http://search.freefind.com/find.html?si=77653038&pid=r&n=0&_charset_=UTF-8&bcd=%C3%B7&query=" + str(year)


class TOPSpider(scrapy.Spider):
    name = "top"

    start_urls = get_start_urls()

    def parse(self, response):
        return self.get_obits(response)

    def get_obits(self, response):
        for link in response.xpath("//table/tr/td/div/font/a"):
            url = link.xpath('@href').extract()[0]
            link_text = "".join(link.xpath('text()').extract())
            link_text_elements = link_text.split("-", 1)
            if len(link_text_elements) == 2:
                item = TOPObitItem()
                item['link'] = url
                item['full_name_raw'] = link_text_elements[1].strip()
                item['date'] = link_text_elements[0].strip()
                yield item
            else:
                print(link, link_text)

        next_page = response.xpath("//a[contains(., 'Next')]/@href")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.get_obits)