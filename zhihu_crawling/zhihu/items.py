# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiveItem(scrapy.Item):
    data = scrapy.Field()
    type = scrapy.Field() # data type: live

class CommentItem(scrapy.Item):
    id = scrapy.Field() # live id
    data = scrapy.Field()
    type = scrapy.Field() # data type: comment
