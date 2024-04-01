# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AuchanItem(scrapy.Item):
    name = scrapy.Field()
    category_name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    volume = scrapy.Field()
    unit = scrapy.Field()
    volume_info = scrapy.Field()
    package_unit = scrapy.Field()
    package_size = scrapy.Field()
