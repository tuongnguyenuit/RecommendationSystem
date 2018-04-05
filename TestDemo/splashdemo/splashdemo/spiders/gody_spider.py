# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""

script2 = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))
    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""


class FahasaSpider(scrapy.Spider):
    name = 'gody'
    allowed_domains = ['gody.vn']
    start_urls = [
        "http://gody.vn/ket-qua-tim-kiem/da-nang?cat=places&_key=5ac48a070b78a417463c9869"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        # Get URL in page and yield Request
        url_selector = response.xpath(
            '//div[@class="item-data"]/a[@class="link-item"]/@href')
        for url in url_selector.extract():
            yield SplashRequest(url, callback=self.parse_item,
                                endpoint='execute',
                                args={'lua_source': script2})

    def parse_item(self, response):
            yield {
                    'Name': response.css('div.container h1.dest-name::text').extract_first(),
                }

        
                


        

