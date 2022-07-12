import time

from demo.mysql.JDBCUtils import JDBCUtils


class articleListData:

    def saveArticle(self, page_id, archive_id, url, name, pic_total, source=1):
        if not self.info(archive_id, source):
            self.save(page_id, archive_id, url, name, pic_total, source)
            print("当前页：%d, 采集文章 id：%d" % (page_id, archive_id))

    def save(self, page_id, archive_id, url, name, pic_total, source=1):
        '''
        保存列表记录
        :param page_id:
        :param archive_id:
        :param url:
        :param name:
        :param pic_total:
        :param source:
        :return:
        '''
        db = JDBCUtils()
        created_at = int(time.time())
        data = [
            page_id, source, archive_id, url, name, pic_total, created_at
        ]
        sql = "insert into crawl_article_list(page_id,source,archive_id,url,name,pic_total,created_at) values (%s, %s, %s, %s, %s, %s, %s)"
        return db.insert(sql, data)

    def batchSave(self, data):
        '''
        保存列表记录
        :param data:
        :return:
        '''
        db = JDBCUtils()
        # created_at = int(time.time())
        # data = [
        #     page_id, source, archive_id, url, name, pic_total, created_at
        # ]
        sql = "insert into crawl_article_list(page_id,source,archive_id,url,name,pic_total,created_at) values (%s, %s, %s, %s, %s, %s, %s)"
        return db.insertmany(sql, data)

    def info(self, archiveId, source=1):
        '''
        获取分页详情
        :param archiveId:  文章 id
        :return:
        '''
        db = JDBCUtils()
        sql = "select * from crawl_article_list where archive_id=%s and source = %s"
        data = [
            archiveId,
            source
        ]
        return db.select(sql, data)

    def getOneUnCrawlUrlBySource(self, source=1):
        '''
        获取一条未采集的 url
        :param source:
        :return:
        '''
        db = JDBCUtils()
        sql = "select * from crawl_article_list where source=%s  and status = 1 limit 1"
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
        sql = "update crawl_article_list set status=%s where id=%s"
        data = [
            status,
            id
        ]
        return db.update(sql, data)
