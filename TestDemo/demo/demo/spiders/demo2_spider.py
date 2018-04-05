from scrapy import Spider
from scrapy.selector import Selector
from demo.items import DemoItem

class Demo2Spider(Spider):
    name = 'demo2'
    allowed_domains = ['vnexpress.net']
    start_urls = [
        "https://giaitri.vnexpress.net/",
    ]

    def parse(self, response):
        item = DemoItem()
        item['title'] = Selector(response).xpath('/html/body/section[2]/article/h1/a[1]/text()').extract()[0]
        item['url'] = Selector(response).xpath('/html/body/section[2]/article/h1/a[1]/@href').extract()[0]
        yield item