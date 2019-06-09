# Zalando Spider
## Getting started
环境要求：
 - MongoDB
 - Scrapy
 - pymongo
 ---
变量设置：

在[zalando\settings.py](./zalando/settings.py)中更改:

 - MongoDB相关变量
 - 能访问的zalando域名（如'https://www.zalando.co.uk'）
 - 需要爬取的类别，具体为该类别主页URL域名后半部分，如'https://www.zalando.co.uk/womens-clothing-coats/'中的'womens-clothing-coats'。不同类用英文逗号隔开，如'womens-clothing-coats-short-coats,womens-clothing-coats-trench-coats'（不要加空格）
 
---
开始爬取信息：

1. 爬取设置的类别下所有衣服的名称及详情页URL，运行:
```
scrapy crawl zalando
```
2. 爬取所有衣服的所有图片URL，衣服图片URL，模特图片URL以及衣服其他颜色的相关信息，运行：
```
scrapy crawl zalando_detail
```