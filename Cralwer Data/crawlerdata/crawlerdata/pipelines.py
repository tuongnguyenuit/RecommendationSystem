# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class CrawlerdataPipeline(object):
#     def process_item(self, item, spider):
#         return item

from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem

class CrawlerdataPipeline(object):

    def __init__(self):
        _engine = create_engine("sqlite:///datademo2.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _stack_items = Table("Test", _metadata,
                             Column("city", Text),
                             Column("category", Text),
                             Column("name", Text),
                             Column("rating", Text),
                             Column("reviews_number", Text),
                             Column("rank", Text),
                             Column("address", Text),
                             Column("avatar", Text),
                             Column("attraction", Text))
        _metadata.create_all(_engine)
        self.connection = _connection
        self.stack_items = _stack_items
    
    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            ins_query = self.stack_items.insert().values(
                city=item["city"],
                category=item["category"], 
                name=item["name"], 
                rating=item["rating"], 
                reviews_number=item["reviews_number"],
                rank=item["rank"],
                address=item["address"],
                avatar=item["avatar"],
                attraction=item["attraction"])
            self.connection.execute(ins_query)
        return item
