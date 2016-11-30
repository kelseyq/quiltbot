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
        for link in response.xpath("//table/tr/td/div/font/a/@href"):
            url = response.urljoin(link.extract())
            yield scrapy.Request(url, callback=self.process_obit)

        next_page = response.xpath("//a[contains(., 'Next')]/@href")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.get_obits)

    def process_obit(self, response):
        title = response.xpath('//title/text()').extract()[0]
        title_elements = title.split("-", 1)
        if len(title_elements) == 2:
            item = TOPObitItem()
            full_name = ""
            try:
                full_name = " ".join(response.xpath('//table//tr/td/div/p[3]/*/*/text()').extract()[0].split())
            except:
                pass
            item['full_name'] = full_name
            item['link'] = response.url
            item['title_name'] = title_elements[1].strip()
            item['date'] = title_elements[0].strip()
            return item
        else:
            print(response.url, title_elements)