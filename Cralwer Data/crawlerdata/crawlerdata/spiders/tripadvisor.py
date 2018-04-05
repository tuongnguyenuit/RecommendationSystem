import scrapy
from scrapy import Spider
from crawlerdata.items import CrawlerdataItem

class TripadvisorSpider(Spider):
    data = {"binh dinh":[]}
    name = 'tripadvisor'
    allowed_domains = ["tripadvisor.com.vn"]
    start_urls = [
        "https://www.tripadvisor.com.vn/Attractions-g608528-Activities-Quy_Nhon_Binh_Dinh_Province.html"
    ]

    def parse(self, response):
        for element in response.css('div.attraction_element'):
            url = element.css('div.listing_title a::attr(href)').extract()[0]           
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_item)

    def parse_item(self, response):
        item = CrawlerdataItem()
        item['location'] = response.css('span.locality::text').extract_first()
        item['rank'] = response.css('span.header_popularity.popIndexValidation b span::text').extract_first()
        item['name'] = response.css('h1.heading_title::text').extract_first()
        item['rating'] = response.css('div.rs.rating span::attr(content)').extract_first()
        item['street_address'] = response.css('span.street-address::text').extract_first() + ', ' + item['location']
        item['reviews_number'] = response.css('div.rs.rating a.more span::text').extract_first()
        yield item
        