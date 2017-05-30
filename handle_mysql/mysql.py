# encoding=utf8
import MySQLdb
import fileinput

class Mysql(object):

    ##配置文件的位置
    MYSQL_CONF = '..//..//mysql.conf'

    ##连接数据库
    def connection_db(self,db_name):
        '''
        数据库链接
        :param db_name: 数据库的名字 
        :return: 返回数据库链接
        '''
        ##配置文件
        conf = {}
        for line in fileinput.input(self.MYSQL_CONF):
            lines = line.replace(' ', '').replace('\n', '').replace('\r', '').split("=")
            conf[lines[0]] = lines[1]
        try:
            conn = MySQLdb.connect(host=conf["IP"], port=int(conf["PORT"]), user=conf["USER_NAME"], passwd=conf["PWD"],
                                   db=db_name, charset='utf8')
            return conn
        except Exception,e:
            print "数据库链接失败!Error:",e

    ##创建数据库
    def create_db(self, db_name):
        '''
        创建数据库
        :param db_name: 数据库名 
        :return: 
        '''
        ##配置文件
        conf = {}
        for line in fileinput.input(self.MYSQL_CONF):
            lines = line.replace(' ', '').replace('\n', '').replace('\r', '').split("=")
            conf[lines[0]] = lines[1]
        ##建立于数据库的链接
        try:
            conn = MySQLdb.connect(host=conf["IP"], port=int(conf["PORT"]), user=conf["USER_NAME"], passwd=conf["PWD"])
            # 获取操作游标
            cursor = conn.cursor()
            # 执行SQL,创建一个数据库.
            cursor.execute("""create database  """ + db_name)
            # 关闭连接，释放资源
            cursor.close();
            print db_name + '数据库创建成功！'
        except Exception, e:
            print db_name + '数据库创建失败！',
            print "Error:", e

    ##插入数据库
    def insert(self,valus):
        db_name = ""
        conn = self.connection_db(db_name)



my = Mysql()
my.create_db('asd')
