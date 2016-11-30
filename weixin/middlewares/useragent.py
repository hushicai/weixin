
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class MyUserAgentMiddleware(UserAgentMiddleware):

  """useragent middleware"""

  def __init__(self, user_agent = ''):
    """@todo: to be defined1. """
    self.user_agent = user_agent


  def process_request(self, request, spider):
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) " \
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"

    if ua:
      request.headers.setdefault('User-Agent', ua)
