import scrapy
import re

class WeixinSpider(scrapy.Spider):
  name = 'weixin'

  download_delay = 2

  allow_domains = ['weixin.sogou.com']

  start_urls = ['http://weixin.sogou.com/weixin?type=2&query=javascript']

  def parse(self, response):
    """parse response"""
    for item in response.xpath('//*[@class="news-list"]/li'):
      title = item.xpath('//h3/a').extract()
      title = re.sub(r'(</?\w+[^>]*>)|(<![^>]*>)', '', title[0])
      yield {
        'title': title
      }

    next_page = response\
      .xpath('//div[@id="pagebar_container"]/a[@id="sogou_next"]/@href')\
      .extract_first()

    if next_page is not None:
      next_page_url = response.urljoin(next_page)
      yield scrapy.Request(next_page_url, callback = self.parse)
