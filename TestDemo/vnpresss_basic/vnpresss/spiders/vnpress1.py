from scrapy import Spider
from scrapy.selector import Selector


class VnpressSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ["tripadvisor.com.vn"]
    start_urls = [
        "https://www.tripadvisor.com.vn/Attractions-g608528-Activities-Quy_Nhon_Binh_Dinh_Province.html"

    ]

    def parse(self, response):
        item = {}
        item['datetime'] = response.xpath('//*[@id="HEADING"]/text()').extract()[0]
        item['author'] = response.xpath('//*[@id="HEADING"]/text()').extract()[0]
        yield item