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
    name = 'diadiemanuong'
    allowed_domains = ['diadiemanuong.com']
    start_urls = [
        "http://diadiemanuong.com/Search?q=&renderStyle=0&s=1&p=1765"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        for hotel in response.css('a.list-item'):
            try:
                yield {
                    'Rating': hotel.css('div.star::attr(data-star-value)').extract_first(),
                    'Name': hotel.css('h3.ddd::text').extract_first(),
                    'Price': hotel.css('span.price::text').extract_first().strip().replace("\n",""),
                    'Address': hotel.css('span.address::text').extract_first().strip(),
                    'Review': hotel.css('span.date::text').extract_first(),
                    'View': hotel.css('div.summary span::text').extract_first(),
                }
            except:
                yield {
                    'Rating': hotel.css('div.star::attr(data-star-value)').extract_first(),
                    'Name': hotel.css('h3.ddd::text').extract_first(),
                    'Price': hotel.css('span.price::text').extract_first().strip().replace("\n",""),
                    'Address': hotel.css('span.address::text').extract_first(),
                    'Review': hotel.css('span.date::text').extract_first(),
                    'View': hotel.css('div.summary span::text').extract_first(),
                }


        # Get the next page and yield Request
        for url in response.xpath('//*[@id="result"]/div[4]/a[last()-1]/@href').extract():
            full_url = response.urljoin(url)
            yield SplashRequest(full_url, self.parse,    
                                endpoint='execute',
                                args={'lua_source': script2})


        

