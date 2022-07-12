import time

from demo.mysql.JDBCUtils import JDBCUtils


class picListData:

    def savePic(self, article_id, pic_url, file_path=''):
        if not self.info(pic_url):
            self.save(article_id, pic_url, file_path)
            print("当前文章：%d, 图片地址 id：%s" % (article_id, pic_url))


    def save(self, article_id, pic_url, file_path=''):
        '''
        保存列表记录
        :param article_id:
        :param pic_url:
        :param file_path:
        :return:
        '''
        db = JDBCUtils()
        created_at = int(time.time())
        data = [
            article_id, pic_url, file_path, created_at
        ]

        sql = "insert into crawl_pic_list(article_id,pic_url,storage_path,created_at) values (%s, %s, %s, %s)"
        return db.insert(sql, data)

    def batchSave(self, data):
        db = JDBCUtils()

        sql = "insert into crawl_pic_list(article_id,pic_url,storage_path,created_at) values (%s, %s, %s, %s)"
        return db.insertmany(sql, data)
    def info(self, pic_url):
        '''
        获取分页详情
        :param pic_url:  图片地址
        :return:
        '''
        db = JDBCUtils()
        sql = "select * from crawl_pic_list where pic_url=%s"
        data = [
            pic_url,
        ]
        return db.select(sql, data)

    def getOneUnCrawlUrlBySource(self, source=1):
        '''
        获取一条未采集的 url
        :param source:
        :return:
        '''
        db = JDBCUtils()
        sql = "select page_url from crawl_pic_list where source=%s  and status = 1 limit 1"
        data = [
            source,
        ]
        return db.select(sql, data)

    def updateStatusById(self, id, status):
        '''
        根据 id 更新采集状态
        :param id:
        :param status:
        :return:
        '''
        db = JDBCUtils()
        sql = "update crawl_pic_list set status=%s where id=%d"
        data = [
            status,
            id
        ]
        return db.update(sql, data)
