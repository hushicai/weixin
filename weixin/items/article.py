#  encoding: utf-8

import scrapy

class AbstractItem(scrapy.Item):

  """微信文章概要"""

  title = scrapy.Field()
  abstract = scrapy.Field()
  account_name = scrapy.Field()

  def __init__(self):
    scrapy.Item.__init__(self)


class DetailItem(scrapy.Item):

  """微信文章详情"""

  link = scrapy.Field()
  content = scrapy.Field()
  publish_time = scrapy.Field(serilizer = str)
  read_count = scrapy.Field()
  like_count = scrapy.Field()

  def __init__(self):
    scrapy.Item.__init__(self)
