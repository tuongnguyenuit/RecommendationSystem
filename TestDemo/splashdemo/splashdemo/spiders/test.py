# -*- coding: utf-8 -*-
import codecs
import json

import scrapy
from scrapy_splash import SplashRequest
import re

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


class hotel(scrapy.Spider):
    name = 'vntrip'
    allowed_domains = ['vntrip.vn']
    start_urls = [
        # "https://www.vntrip.vn/khach-san/ha-noi",
        "https://www.vntrip.vn/khach-san/da-nang",
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        filename = 'vntrip.json'

        for hotel in response.css('div.prdItem'):
            yield {
                'Name': hotel.css('div.info-name a::text').extract_first(),
                'Price': hotel.css('div.itemPrice.hidden-xs p.price-number::text').extract()
            }
            #print(item)
            # self.data['hotel'].append(item)

        # with codecs.open(filename, "w+", encoding="utf-8") as f:
        #     json.dump(self.data, f, ensure_ascii=False)
        # self.log('Saved file %s' % filename)

        # Get the next page and yield Request
        next_selector = response.css('li.next a::attr(href)')
        for url in next_selector.extract():
            yield SplashRequest(url, endpoint='execute',callback=self.parse,
                                args={'lua_source': script2})

                                
    def next_select(self,response):
        next_selector = response.css('li.next a::attr(href)')
        for url in next_selector.extract():
            yield SplashRequest(url, endpoint='execute', callback=self.parse_item,
                                args={'lua_source': script2})

    def parse_item(self, response):
        filename = 'vntrip.json'
        for hotel in response.css('div.prdItem'):
            yield {
                'Name': hotel.css('div.info-name a::text').extract_first(),
                'Rating': hotel.css('div.info-name div.hotel-rating span.text-start i.number::text').extract_first(),
                'Address': hotel.css('div.prAddress::text').extract_first(),
                'Facilities': hotel.css('ul.default-facilities li::text').extract(),
                'Price': hotel.css('div.itemPrice.hidden-xs p.price-number::text').extract()
            }