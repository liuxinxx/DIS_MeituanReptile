#encoding=utf8
'''
获取城市列表，并添加到消息队列中
将任务添加到RabbitMQ消息队列
    
'''
import pika
import time
import HTMLParser
import fileinput
import requests
from bs4 import BeautifulSoup
class City(object):
    def downloader_html(self,url):##利用PhantomJS获取网页数据
        BAIDU_UA = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'#百度爬虫UA
        headers = {'User-Agent': BAIDU_UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
        data = requests.get(url, headers=headers) ##这样服务器就会以为我们是真的浏览器了
        html_parser = HTMLParser.HTMLParser()
        data = html_parser.unescape(data.text)   
        return data
    def ff(self):
        print ""
    def getCityList(self,soup):##获取全国各个地区链接
        soup = BeautifulSoup(soup,'lxml')
        city_List = []    
        div_list = soup.find_all("a",attrs={'gaevent':'changecity/build'})
        for v in div_list:
            city_Name=v.get_text()
            city_Url = v.get('href')  
            ##将数据拼接成JSON数据格式
            cityData="{\"Name\":\""+city_Name+"\",\"Url\":\""+city_Url+"\"}"
            print cityData
            city_List.append(cityData)  
        return city_List
    def send(self,message_list,username,pwd,ip,post):
        '''
        message_list    :消息队列
        '''
        user_pwd = pika.PlainCredentials(username, pwd)
        s_conn = pika.BlockingConnection(pika.ConnectionParameters(ip,post,'/', credentials=user_pwd))#创建连接
        channel = s_conn.channel()  #在连接上创建一个频道
        
        channel.queue_declare(queue='city_task_queue', durable=True) #创建一个新队列task_queue，设置队列持久化，注意不要跟已存在的队列重名，否则有报错
        print '获取到的城市数量:',len(message_list)
        for g in  range(len(message_list)):
            message = message_list[g]
            message = message.encode('utf-8')
            channel.basic_publish(exchange='',
                                  routing_key='city_task_queue',#写明将消息发送给队列worker
                                  body=message,    #要发送的消息
                                  properties=pika.BasicProperties(delivery_mode=2,)#设置消息持久化，将要发送的消息的属性标记为2，表示该消息要持久化
                                  )
            print g,':',message
            time.sleep(0.02)#设置延迟
        print g
if __name__ == '__main__':
##配置文件中读取RabbitMQ服务器的配置信息USER_NAME,PWD,IP,POST
#     USER_NAME = username
#     PWD = password
#     IP = ip
#     POST = post
    conf = {}
    for line in fileinput.input("..//..//RabbitMQ_Server.conf"):
        lines = line.replace(' ','').replace('\n','').split("=")
        conf[lines[0]] = lines[1]
    CITY_URL = 'http://www.meituan.com/index/changecity/initiative'
    city = City()
    soup = city.downloader_html(CITY_URL)
    message_list = city.getCityList(soup)
    city.send(message_list,conf["USER_NAME"],conf["PWD"],conf["IP"],conf["POST"])
  