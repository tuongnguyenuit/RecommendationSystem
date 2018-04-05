import scrapy
from scrapy import Spider
from crawlerdata.items import CrawlerdataItem


class TripadvisorSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ["tripadvisor.com.vn"]
    def start_requests(self):
        list_url = [
            # 'https://www.tripadvisor.com.vn/Attractions-g608528-Activities-Quy_Nhon_Binh_Dinh_Province.html',
            # 'https://www.tripadvisor.com.vn/Attractions-g303946-Activities-Vung_Tau_Ba_Ria_Vung_Tau_Province.html',
            # "https://www.tripadvisor.com.vn/Attractions-g293925-Activities-Ho_Chi_Minh_City.html",
            "https://www.tripadvisor.com.vn/Attractions-g293925-Activities-c42-Ho_Chi_Minh_City.html#FILTERED_LIST"

        ]
        for url in list_url:
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        # Get url of category

        # Get url of next page
        for nextpage in response.css('div.al_border.deckTools.btm > div > div > a::attr(href)').extract()[0]:
            full_url = response.urljoin(nextpage)
            yield scrapy.Request(full_url)            

        # Get url of element in page
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
        item['street_address'] = response.css('span.street-address::text').extract_first()
        item['reviews_number'] = response.css('div.rs.rating a.more span::text').extract_first()
        yield item
        