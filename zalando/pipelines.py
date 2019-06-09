# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class ZalandoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        if settings['MONGO_USER'] and settings['MONGO_PSW']:
            self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        postItem = dict(item)
        url = {'detail_url': postItem['detail_url']}
        if not self.coll.find_one(url):
            self.coll.insert(postItem)
        else:
            self.coll.update_one(url, {'$set': postItem, '$currentDate': {'lastModified': True}})
        # return item
