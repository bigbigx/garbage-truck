import scrapy
from dongying.items import DongyingItem

class MM(scrapy.Spider):
    name = 'mm'

    start_urls = ['http://www.juemei.com/mm/sfz/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.waterfall').css('a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_mm)

        # follow pagination links
        next_page = response.css('.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_mm(self, response):
        item = DongyingItem()
        item['titles'] = response.css('h1::text').extract_first()
        item['urls'] = response.url
        item['image_urls'] = response.css('.wrap>img::attr(src)').extract()
        yield item