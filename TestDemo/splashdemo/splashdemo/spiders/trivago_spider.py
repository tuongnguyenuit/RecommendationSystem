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
    name = 'trivago'
    allowed_domains = ['trivago.vn']
    start_urls = [
        "https://www.trivago.vn/?aDateRange%5Barr%5D=2018-04-14&aDateRange%5Bdep%5D=2018-04-15&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iPathId=531162"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        for hotel in response.css('div.pos-relative item__wrapper'):
            yield {
                'Name': hotel.css('h3.name__copytext m-0 item__slideout-toggle::text').extract_first(),
                'Rating': hotel.css('span.rating-box__value::text').extract_first(),
                'Address': hotel.css('span.item__distance::text').extract_first().strip(),
                'Price': hotel.css('strong.item__best-price mb-gutter-quarter price single long_digit::text').extract_first().strip().replace("\n",""),
                'Review': hotel.css('span.review__count::text').extract_first(),
                #'View': hotel.css('div.summary span::text').extract_first(),
            }

        # Get the next page and yield Request
        for url in response.xpath('//*[@id="js_item_list_section"]/div[1]/button').extract():
            full_url = response.urljoin(url)
            yield SplashRequest(full_url, self.parse,    
                                endpoint='execute',
                                args={'lua_source': script2})


        

