#encoding=utf8
import pika
import time
import json
import fileinput
import requests
import HTMLParser
from bs4 import BeautifulSoup
from task_send import taskList_MQ
class ShopClass(object):
    def __init__(self):
        self.downloader = taskList_MQ.City
    def shop_class(self,soup):
        print len(soup)
        list_fenlei = []    
        div_list = soup.find_all("div",class_="J-nav-item")
        for v in div_list:
            for k in v.find_all('li'):
                k = k.find('a')        
                fenlei_url =k.get('href')
                fenlei_name =k.get_text()
                list_fenlei.append([fenlei_name,fenlei_url])           
        return list_fenlei
    def downloader_html(self,url):
        ##利用PhantomJS获取网页数据
        BAIDU_UA = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'#百度爬虫UA
        headers = {'User-Agent': BAIDU_UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
        data = requests.get(url, headers=headers) ##这样服务器就会以为我们是真的浏览器了
        html_parser = HTMLParser.HTMLParser()
        data = html_parser.unescape(data.text)   
        return data
    def write(self,str,file_name,flag):#将制定的字符串写入指定的文件中，当标记flag为1时，代表追加写入，为2时代表清除源文件后写入
        if flag == 1:
            file_object = open(file_name, 'a')
            file_object.write(str)
            file_object.close()
        if flag ==2:
            file_object = open(file_name, 'wb')
            file_object.write(str)
            file_object.close()
    def callback(self,ch, method, properties, body):
            print body.decode('utf-8')#字节转字符串
            data = json.loads(body.decode('utf8'))
            city_url =  data['Url']#获取城市URL
            city_name = data['Name']#获取城市名字
            data = self.downloader_html(city_url).encode("utf8")
            print len(data)
            soup = BeautifulSoup(data,'lxml')  
            shopClassList = self.shop_class(soup)
            for g in shopClassList:
                print g[0].encode("utf8"),g[1].encode("utf8")
            time.sleep(10)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print '解析完成'
    def receive(self,username,pwd,ip,post):#处理城市队列，将每个城市获取到的分类信息打印出来
        user_pwd = pika.PlainCredentials(username, pwd)
        s_conn = pika.BlockingConnection(pika.ConnectionParameters(ip,post,'/', credentials=user_pwd))
        channel = s_conn.channel()  
        channel.queue_declare(queue='city_task_queue', durable=True) 
        channel.basic_qos(prefetch_count=1) 
        print '开始解析该地区商家分类'        
        channel.basic_consume(self.callback,
                              queue='city_task_queue',
                              )
        channel.start_consuming()
if __name__ == '__main__':
    conf = {}
    for line in fileinput.input("..//RabbitMQ_Server.conf"):
        lines = line.replace(' ','').replace('\n','').split("=")
        conf[lines[0]] = lines[1]     
    shop = ShopClass()
    soup = shop.receive(conf["USER_NAME"],conf["PWD"],conf["IP"],conf["POST"])
