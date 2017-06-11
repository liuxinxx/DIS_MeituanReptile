#encoding=utf8
import pika
'''
从指定消息队列中获取到任务
回调函数作为参数
'''
class Receive(object):
    def receive(self,callback, username, pwd, ip, port):
        '''
        # 处理城市队列，将每个城市获取到的分类信息打印出来
        :param callback: 回调函数
        :param username: 远程RabbitMQ服务器的用户名
        :param pwd:      密码
        :param ip:      ip
        :param port:    端口
        :return:        
        '''
        user_pwd = pika.PlainCredentials(username, pwd)
        s_conn = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials=user_pwd))
        channel = s_conn.channel()
        channel.queue_declare(queue='city_task_queue', durable=True)
        channel.basic_qos(prefetch_count=1)
        print '开始解析该地区商家分类'
        channel.basic_consume(callback,
                              queue='city_task_queue',
                              )
        channel.start_consuming()