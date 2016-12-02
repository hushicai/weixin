#  encoding: utf-8

import scrapy

class Item(scrapy.Item):

  """微信文章信息"""

  title = scrapy.Field()
  abstract = scrapy.Field()
  account_name = scrapy.Field()
  publish_time = scrapy.Field(serilizer = str)
  content = scrapy.Field()
  author = scrapy.Field()
  read_count = scrapy.Field()
  praise_count = scrapy.Field()

  def __init__(self):
    scrapy.Item.__init__(self)
