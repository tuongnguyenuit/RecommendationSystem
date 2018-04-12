import scrapy
from scrapy import Spider
from crawlerdata.items import CrawlerdataItem


class TripadvisorSpider(Spider):
    name = 'tripadvisor'
    allowed_domains = ["tripadvisor.com.vn"]
    def start_requests(self):
        list_url = [
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c42-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c47-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c61-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c55-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c36-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c49-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c57-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c58-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c40-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c59-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c26-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c41-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c20-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c56-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c60-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c52-Hanoi.html",
            #"https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c48-Hanoi.html",
            "https://www.tripadvisor.com.vn/Attractions-g293924-Activities-c62-Hanoi.html",
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
        try:
            # Case 1: Have 3 attraction and long address
            item = CrawlerdataItem()
            item['category'] = "Sự kiện"
            item['name'] = response.css('h1.heading_title::text').extract_first()        
            item['rating'] = response.css('div.rs.rating span::attr(content)').extract_first()
            item['reviews_number'] = response.css('div.rs.rating a.more span::text').extract_first()
            item['rank'] = response.css('span.header_popularity.popIndexValidation b span::text').extract_first().replace("Số ", "")
            item['address'] = response.css('span.street-address::text').extract_first() + ", " + response.css('span.locality::text').extract_first().replace(", ", "")
            item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
            item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[2]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[3]/text()').extract_first()
            yield item            
        except:
            try:       
                # Case 2: Have 2 attraction and long address           
                item['address'] = response.css('span.street-address::text').extract_first() + ", " + response.css('span.locality::text').extract_first().replace(", ", "")
                item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
                item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[2]/text()').extract_first()
                yield item
            except:
                try:
                    # Case 3: Have 3 attraction and short address
                    item['address'] = response.css('span.locality::text').extract_first().replace(", ", "")
                    item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
                    item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[2]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[3]/text()').extract_first()
                    yield item
                except:
                    try:
                        # Case 4: Have 2 attraction and short address         
                        item['address'] = response.css('span.locality::text').extract_first().replace(", ", "")
                        item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
                        item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first() + ", " + response.xpath('//span[@class="header_detail attraction_details"]/div/a[2]/text()').extract_first()
                        yield item
                    except:
                        try:
                            # Case 5: Have 1 attraction and long address
                            item['address'] = response.css('span.street-address::text').extract_first() + ", " + response.css('span.locality::text').extract_first().replace(", ", "")
                            item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
                            item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first()
                            yield item
                        except:
                            # Case 6: Have 1 attraction and short address
                            item['address'] = response.css('span.locality::text').extract_first().replace(", ", "")
                            item['avatar'] = response.xpath('//*[@id="taplc_location_detail_above_the_fold_attractions_0"]/div/div[3]/div[1]/div/div/div[1]/div/div/div/div[1]/div[last()]/span/img/@src').extract_first()
                            item['attraction'] = response.xpath('//span[@class="header_detail attraction_details"]/div/a[1]/text()').extract_first()
                            yield item



        # category = scrapy.Field()
        # name = scrapy.Field()    
        # rating = scrapy.Field()
        # reviews_number = scrapy.Field()
        # rank = scrapy.Field()
        # address = scrapy.Field()
        # avatar = scrapy.Field()
        # attraction = scrapy.Field()



     
        