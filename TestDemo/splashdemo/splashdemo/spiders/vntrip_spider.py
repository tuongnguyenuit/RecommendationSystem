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
    name = 'vntrip22'
    allowed_domains = ['vntrip.vn']
    start_urls = [
        "https://www.vntrip.vn/khach-san/da-nang"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        for hotel in response.css('div.prdItem'):
            yield {
                'Name': hotel.css('div.info-name a::text').extract_first(),
                'Rating': hotel.css('span.text-start i.number::text').extract_first(),
                'Address': hotel.css('div.prAddress::text').extract_first().strip(),
                'Price': hotel.css('div.iPrice p.price-number::text').extract(),
            }

        # Get the next page and yield Request
        for url in response.css('li.next a::attr(href)').extract():
            yield SplashRequest(url, self.parse,
                                endpoint='execute',
                                args={'lua_source': script2})


        

