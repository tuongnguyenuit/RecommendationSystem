from scrapy import Spider
from scrapy.selector import Selector
from demo.items import DemoItem

class TikiSpider(Spider):
    name = 'tiki'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        "http://webcache.googleusercontent.com/search?q=cache:http%3A%2F%2Fquotes.toscrape.com%2Fjs%2F",
    ]

    def parse(self, response):
        item = DemoItem()          
        item['title'] = Selector(response).xpath(
                '//div[@class="quote"]/span[@class="text"]/text()').extract()[0]
        yield item