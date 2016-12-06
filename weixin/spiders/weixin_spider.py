
#  enocoding: utf-8

import re
import scrapy
from bs4 import BeautifulSoup
from urllib import urlencode
# relative import只能用在toplevel空间中
from weixin.items import *
from hashlib import md5

class WeixinSpider(scrapy.Spider):
  name = 'weixin'

  download_delay = 2

  start_urls = ['http://weixin.sogou.com/weixin?type=2&query=javascript']

  def parse(self, response):
    """
    parse搜索列表
    """
    for item in response.xpath('//*[@class="news-list"]/li'):
      title = "".join(item.xpath('.//h3/a/node()').extract())
      abstract = "".join(item.xpath('.//p[@class="txt-info"]/node()').extract())
      #  搜狗时效性链接
      article_temp_link = item.xpath('.//h3/a/@href').extract_first()
      #  账号名
      weixin_name = item.xpath('.//div[@class="s-p"]/a/text()').extract_first()
      weixin_id = item.xpath('.//div[@class="s-p"]/a/@data-username').extract_first()

      raw_title = re.sub('<[^>]*>', '', title).encode('utf-8')

      fd = md5()
      fd.update(weixin_id + ', ')
      fd.update(raw_title)
      uid = fd.hexdigest()

      meta = {
        'article_title': title,
        'article_abstract': abstract,
        'article_weixin_name': weixin_name,
        'article_weixin_id': weixin_id,
        'article_uid': uid
      }

      if article_temp_link is not None:
          yield scrapy.Request(
            article_temp_link,
            callback = self.parse_detail,
            meta = meta
          )

    #  next_page = response\
      #  .xpath('//div[@id="pagebar_container"]/a[@id="sogou_next"]/@href')\
      #  .extract_first()

    #  if next_page is not None:
      #  next_page_url = response.urljoin(next_page)
      #  yield scrapy.Request(next_page_url, callback = self.parse)

  def parse_detail(self, response):
    """parse文章详情"""
    meta = response.meta

    article_item = article.Item()

    article_item['weixin_name'] = meta['article_weixin_name']
    article_item['weixin_id'] = meta['article_weixin_id']
    article_item['title'] = self.remove_highlight_tag(meta['article_title'])
    article_item['uid'] = meta['article_uid']
    article_item['abstract'] =self.remove_highlight_tag(meta['article_abstract'])
    article_item['author'] = response.xpath('//*[@id="img-content"]/div[1]/em[2]/text()').extract_first()
    article_item['content'] = "".join(response.xpath('//*[@id="js_content"]/node()').extract()).strip()
    article_item['publish_time'] = response.xpath('//*[@id="img-content"]/div[1]/em[1]/text()').extract_first()
    article_item['query'] = 'JavaScript'
    article_item['source'] = 'weixin'

    yield article_item

  def remove_highlight_tag(self, value):
    pattern = r'<em><!--red_beg-->([^<>]*?)<!--red_end--><\/em>'
    return re.sub(pattern, '\g<1>', value)
