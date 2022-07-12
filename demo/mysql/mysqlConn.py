'''
连接池初始化模块，做了什么
1、设置类变量 pool 池，
2、设置方法 getconn ，作用通过 dbutils 模块的 PooledDB 方法连接数据库，给 pool 赋值
3、设置方法 getMyConn，返回自身实例对象
核心作用：创建一个类，此类可以创建一个连接池 pool
'''
from dbutils.pooled_db import PooledDB
import pymysql

# import db_config as config

"""
@功能：创建数据库连接池
"""

# 数据库信息
DB_TEST_HOST = "162.14.66.215"
DB_TEST_PORT = 3306
DB_TEST_USER = "root"
DB_TEST_PASSWORD = "dujunlove1314"
DB_TEST_DBNAME = "tools"

# 数据库连接编码
DB_CHARSET = "utf8"

# mincached : 启动时开启的闲置连接数量(缺省值 0 开始时不创建连接)
DB_MIN_CACHED = 20

# maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
DB_MAX_CACHED = 20

# maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
DB_MAX_SHARED = 40

# maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
DB_MAX_CONNECYIONS = 100

# blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......> 其他代表阻塞直到连接数减少,连接被分配)
DB_BLOCKING = True

# maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE = 0

# setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
DB_SET_SESSION = None

# creator : 使用连接数据库的模块
DB_CREATOR = pymysql


class MyConnectionPool(object):
    __pool = None

    # def __init__(self):
    #     self.conn = self.__getConn()
    #     self.cursor = self.conn.cursor()

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=DB_CREATOR,
                mincached=DB_MIN_CACHED,
                maxcached=DB_MAX_CACHED,
                maxshared=DB_MAX_SHARED,
                maxconnections=DB_MAX_CONNECYIONS,
                blocking=DB_BLOCKING,
                maxusage=DB_MAX_USAGE,
                setsession=DB_SET_SESSION,
                host=DB_TEST_HOST,
                port=DB_TEST_PORT,
                user=DB_TEST_USER,
                passwd=DB_TEST_PASSWORD,
                db=DB_TEST_DBNAME,
                use_unicode=True,
                charset=DB_CHARSET
            )
        return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # 关闭连接归还给链接池
    # def close(self):
    #     self.cursor.close()
    #     self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn


# 获取连接池,实例化
def get_my_connection():
    return MyConnectionPool()
