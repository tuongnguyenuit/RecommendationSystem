# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerdataItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    reviews_number = scrapy.Field()
    rank = scrapy.Field()
    street_address = scrapy.Field()
    location = scrapy.Field()

    
