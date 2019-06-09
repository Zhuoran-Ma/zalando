# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZalandoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    detail_url = scrapy.Field()
    img_url = scrapy.Field()
    model_url = scrapy.Field()
    cloth_img_url = scrapy.Field()

    pass
