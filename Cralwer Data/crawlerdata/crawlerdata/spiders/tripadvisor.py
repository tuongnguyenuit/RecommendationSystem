import scrapy
from scrapy import Spider
from crawlerdata.items import CrawlerdataItem


class TripadvisorSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ["tripadvisor.com.vn"]
    def start_requests(self):
        list_url = [
            "https://www.tripadvisor.com.vn/Attractions-g293925-Activities-c47-Ho_Chi_Minh_City.html",

        ]
        for url in list_url:
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):     
        # Get url of next page
        for nextpage in response.css('#FILTERED_LIST > div.al_border.deckTools.btm > div > div > a.nav.next.rndBtn.ui_button.primary.taLnk::attr(href)').extract():
            full_url = response.urljoin(nextpage)
            yield scrapy.Request(full_url)

        # Get url of element in page
        for element in response.css('div.attraction_element'):
            url = element.css('div.listing_title a::attr(href)').extract()[0]           
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_item)


    def parse_item(self, response):
        item = CrawlerdataItem()
        item['category'] = "Danh lam & Thắng cảnh"
        item['name'] = response.css('h1.heading_title::text').extract_first()        
        item['rank'] = response.css('span.header_popularity.popIndexValidation b span::text').extract_first().replace("Số ", "")
        item['rating'] = response.css('div.rs.rating span::attr(content)').extract_first()
        item['reviews_number'] = response.css('div.rs.rating a.more span::text').extract_first()
        # item['address'] = response.css('span.street-address::text').extract_first() + ", " + response.css('span.locality::text').extract_first().replace(", ", "")
        # item['open_time'] = response.css('div.ui_column.is-12 span[1]::text')
        yield item

        # category = scrapy.Field()
        # name = scrapy.Field()    
        # rating = scrapy.Field()
        # reviews_number = scrapy.Field()
        # rank = scrapy.Field()
        # address = scrapy.Field()
        # open_time = scrapy.Field()
        # avatar = scrapy.Field()
        # attraction = scrapy.Field()



     
        