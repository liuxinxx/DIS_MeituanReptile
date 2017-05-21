#encoding=utf8
import pika
import time
class Send(object):
    def send(self, message_list, username, pwd, ip, port,queue_name):
        '''
        发送指定消息到指定队列中
        :param message_list 消息队列
        :param username     远程RabbitMQ服务器用户名
        :param pwd          密码
        :param ip           远程服务器ip
        :param port         端口
        :param queue_name   指定将消息放入的队列
        :return 
        '''
        user_pwd = pika.PlainCredentials(username, pwd)
        s_conn = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', credentials=user_pwd))  # 创建连接
        channel = s_conn.channel()  # 在连接上创建一个频道

        channel.queue_declare(queue=queue_name, durable=True)  # 创建一个新队列task_queue，设置队列持久化，注意不要跟已存在的队列重名，否则有报错
        print '要添加到任务队列的数量:', len(message_list)
        for g in range(len(message_list)):
            message = message_list[g]
            message = message.encode('utf-8')#将字符转化为字符串，存入到消息队列中
            channel.basic_publish(exchange='',
                                  routing_key=queue_name,  # 写明将消息发送给队列worker
                                  body=message,  # 要发送的消息
                                  properties=pika.BasicProperties(delivery_mode=2, )  # 设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                                  )
            print g, ':', message
            time.sleep(0.02)  # 设置延迟
        print g