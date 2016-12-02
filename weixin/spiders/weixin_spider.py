
#  enocoding: utf-8

import scrapy

# relative import只能用在toplevel空间中

from weixin.items import *

print dir()

class WeixinSpider(scrapy.Spider):
  name = 'weixin'

  download_delay = 2

  start_urls = ['http://weixin.sogou.com/weixin?type=2&query=javascript']

  def parse(self, response):
    """
    parse搜索列表
    """
    for item in response.xpath('//*[@class="news-list"]/li'):
      title = "".join(item.xpath('div[2]/h3/a/node()').extract())
      abstract = "".join(item.xpath('div[2]/p/node()').extract())
      account_name = item.xpath('div[2]/div/a[1]/text()').extract_first()
      account_temp_link = item.xpath('div[2]/div/a[1]/@href').extract_first()

      if account_temp_link is not None:
        yield scrapy.Request(
          account_temp_link,
          callback = self.parse_detail
        );


      abstract_article_item = article.AbstractItem()
      abstract_article_item['title'] = title
      abstract_article_item['abstract'] = abstract
      abstract_article_item['account_name'] = account_name

      yield abstract_article_item

    next_page = response\
      .xpath('//div[@id="pagebar_container"]/a[@id="sogou_next"]/@href')\
      .extract_first()

    if next_page is not None:
      next_page_url = response.urljoin(next_page)
      yield scrapy.Request(next_page_url, callback = self.parse)


  def parse_detail(self, response):
    """parse文章详情页"""
    account_name = ''
    link = ''
    content = ''
    publish_time = ''
    read_count = ''
    like_count = ''

    yield {
      'account_name': '',
      'link': link
    }
