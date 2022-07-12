import time

from demo.mysql.JDBCUtils import JDBCUtils


class pageListData:

    def tableName(self):
        return 'crawl_page_list'

    def save(self, page, pageUrl, cate):
        '''
        保存列表记录
        :param page:
        :param pageUrl:
        :param cate:
        :return:
        '''
        db = JDBCUtils()
        data = [
            self.tableName(),
            page,
            pageUrl,
            cate,
            1,
            int(time.time())
        ]
        sql = "insert into `%s`(page,page_url,type,source,created_at) values (%s, %s, %s, %s, %s)"
        return db.insert(sql, data)

    def info(self, cate, page):
        '''
        获取分页详情
        :param cate:  当前网站分类
        :param page: 页数
        :return:
        '''
        db = JDBCUtils()
        sql = "select * from `%s` where type=%s and page=%s and source = 1"
        data = [
            self.tableName(),
            cate,
            page
        ]
        return db.select(sql, data)

    def getOneUnCrawlUrlByCate(self, cate):
        '''
        获取一条未采集的 url
        :param cate:
        :return:
        '''
        db = JDBCUtils()
        sql = "select * from crawl_page_list where type=%s and source = 1 and status = 1 order by page asc limit 1"
        data = [
            cate,
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
        sql = "update crawl_page_list set status=%s where id=%s"
        data = [
            status,
            id
        ]
        return db.update(sql, data)
