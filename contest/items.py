# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ContestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id = scrapy.Field()
    text = scrapy.Field()
    stock = scrapy.Field()
