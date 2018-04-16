# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
IMAGES_URLS_FIELD = 'field_name_for_your_images_urls'
IMAGES_RESULT_FIELD = 'field_name_for_your_processed_images'
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
MEDIA_ALLOW_REDIRECTS = True

class CrawlimagePipeline(object):
    def process_item(self, item, spider):
        return item



