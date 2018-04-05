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
    name = 'google'
    start_urls = [
        "https://www.google.com.vn/destination/map/topsights?q=Các%20địa%20điểm%20ưa%20thích&sa=X&site=search&output=search&dest_mid=%2Fm%2F0hn4h&dest_mid=%2Fm%2F0hn4h&tcfs"
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, response):
        for hotel in response.css('div.eie4Pc'):
            yield {
                    'Name': hotel.css('h2.NbdpWc::text').extract_first(),
                }

        
                


        

