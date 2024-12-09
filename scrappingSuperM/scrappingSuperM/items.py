# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
   name = scrapy.Field()
   actualPrice = scrapy.Field()
   oldPrice = scrapy.Field()
   brand = scrapy.Field()
   supermarket = scrapy.Field()
   tipe = scrapy.Field()
   promotion = scrapy.Field()