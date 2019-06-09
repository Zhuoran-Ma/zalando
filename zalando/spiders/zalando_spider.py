import pymongo
import scrapy
from scrapy.conf import settings

from zalando.items import ZalandoItem


class ZalandoSpider(scrapy.Spider):
    name = 'zalando'
    start_urls = [settings['ZALANDO_DOMAIN_URL'] + '/' + cate for cate in settings['CATEGORY']]

    def parse(self, response):
        item = ZalandoItem()
        clothes = response.xpath(
            '//*[@id="z-nvg-cognac-root"]/div[1]/z-grid/z-grid-item[2]/div/div[5]/z-grid/z-grid-item')
        for cloth in clothes:
            if cloth.xpath('.//div/div/a/div[1]/div[1]/text()'):
                item['name'] = '{} {}'.format(cloth.xpath('.//div/div/a/div[1]/div[1]/text()').get(),
                                              cloth.xpath('.//div/div/a/div[1]/div[2]/text()').get())
                item['detail_url'] = settings['ZALANDO_DOMAIN_URL'] + cloth.xpath('.//div/a[1]/@href').get()
                yield item

        next_page = response.xpath(
            '//*[@id="z-nvg-cognac-root"]/div[1]/z-grid/z-grid-item[2]/div/div[5]/z-grid-item/div/a[2]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


class ZalandoDetailSpider(scrapy.Spider):
    name = 'zalando_detail'

    def __init__(self):
        super(ZalandoDetailSpider, self).__init__()
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        if settings['MONGO_USER'] and settings['MONGO_PSW']:
            self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def start_requests(self):
        for doc in self.coll.find({'img_url': None}):
            yield scrapy.Request(url=doc['detail_url'], callback=self.parse)

    def parse(self, response):
        item = ZalandoItem()
        item['img_url'] = list()
        imgs = response.xpath('//*[@id="topsection-thumbnail-scroller"]/div')
        for img in imgs:
            img = img.xpath('.//div/div/button/div/picture/img/@src').get()
            if 'pack' in img:  # cloth_img
                cloth_img = img.split('/article-image-mhq/')[1].split('?')[0]
                cloth_img = 'https://mosaic01.ztat.net/vgs/media/pdp-zoom/' + cloth_img
                item['cloth_img_url'] = cloth_img
            try:  # 详情中可能会有视频代替图片
                img = img.split('/article-image-mhq/')[1].split('?')[0]
            except:
                pass
            img = 'https://mosaic01.ztat.net/vgs/media/pdp-zoom/' + img
            item['img_url'].append(img)
        if item['img_url']:
            item['model_url'] = item['img_url'][0]
        item['name'] = response.xpath(
            '//*[@id="topsection-thumbnail-scroller"]/div[1]/div/div/button/div/picture/img/@alt').get()
        item['detail_url'] = response.url
        yield item

        other_colors = response.xpath('//*[@id="topsection-color-scroller"]/div')
        if other_colors:
            for color in other_colors:
                color = color.xpath('.//div/div/a/@href').get()
                color = response.urljoin(color)
                yield scrapy.Request(color, callback=self.parse)
