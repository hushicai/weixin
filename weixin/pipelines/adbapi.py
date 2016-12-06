#  encoding: utf-8
import MySQLdb
import MySQLdb.cursors
import logging
import time
from twisted.enterprise import adbapi
from weixin.utilities.decorators import check_spider_pipeline

class WeixinArticlePipeline(object):

  def open_spider(self, spider):
    db_args = dict(
      host = 'localhost',
      user = 'root',
      passwd = '515224',
      db = 'db_weixin',
      charset = 'utf8',
      cursorclass = MySQLdb.cursors.DictCursor,
      use_unicode= True,
    )
    dbpool = adbapi.ConnectionPool('MySQLdb', **db_args)
    self.dbpool = dbpool

  def close_spider(self, spider):
    self.dbpool.close()

  @check_spider_pipeline
  def process_item(self, item, spider):
    deferred = self.dbpool.runInteraction(self._do_interaction, item, spider)
    deferred.addCallback(self._handle_qr_code)
    deferred.addErrback(self._handle_error, item, spider)
    deferred.addBoth(lambda _: item)
    return deferred

  def _do_interaction(self, transaction, item, spider):
    account_id = self._check_account(transaction, item)

    if account_id is None:
      account_id = self._insert_account(transaction, item)

    item['account_id'] = account_id
    self._insert_or_update_article(transaction, item)

  def _insert_or_update_article(self, transaction, item):
    """插入或者更新文章"""
    sql = """select * from db_weixin.tb_weixin_article where uid = %s"""
    transaction.execute(sql, (item['uid'], ))
    ret = transaction.fetchone()

    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    if ret is None:
      # 插入文章
      logging.info('insert article: %s', (item['title']))
      sql = """insert into
      db_weixin.tb_weixin_article(
        uid,
        account_id,
        title,
        abstract,
        content,
        author,
        publish_time,
        query,
        source,
        insert_time
      )
      values(%s,%d,%s,%s,%s,%s,%s,%s,%s,%s)"""
      transaction.execute(
        sql,
        (
          item['uid'],
          item['account_id'],
          item['title'],
          item['abstract'],
          item['content'],
          item['author'],
          item['publish_time'],
          item['query'],
          item['source'],
          nowTime
        )
      )
    else:
      # 更新文章
      logging.info('update article: %s', (item['title']))
      sql = """update db_weixin.tb_weixin_article
      set abstract = %s,content = %s, author= %s, update_time = %s
      where uid = %s
      """
      transaction.execute(
        sql,
        (
          item['abstract'],
          item['content'],
          item['author'],
          nowTime,
          item['uid']
        )
      )

  def _check_account(self, transaction, item):
    """判断微信账号是否已经存在"""
    sql = """select * from db_weixin.tb_weixin_account where weixin_id = %s"""
    transaction.execute(sql, (item['weixin_id'], ))
    ret = transaction.fetchone()
    if ret is None:
      return None
    return ret['id']

  def _insert_account(self, transaction, item):
    """插入新的微信账号"""
    sql = """insert into db_weixin.tb_weixin_account(weixin_id,weixin_name,insert_time)
    values(%s,%s,%s)
    """
    logging.info('insert account: %s', item['weixin_name'])
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    transaction.execute(
      sql,
      (item['weixin_id'], item['weixin_name'],nowTime)
    )
    account_id = transaction.connection.insert_id()
    return account_id

  def _handle_qr_code(self, item):
    """处理二维码
    """

  def _handle_error(self, failure, item, spider):
    logging.info('adbapi runInteraction fail: %s', failure)
