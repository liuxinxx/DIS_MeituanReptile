#encoding=utf8
import pika
import time
import json
import fileinput
import requests
import HTMLParser
from handle_html import handle_html
from bs4 import BeautifulSoup
from task_send import taskList_MQ
from rabbitmq_queues import receive
class ShopClass(object):
    def __init__(self):
        self.html = handle_html.Handle_html()
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
            #print body.decode('utf-8')#字节转字符串
            data = json.loads(body)
            city_url =  data['Url']#获取城市URL
            city_name = data['Name']#获取城市名字
            data = self.html.downloader_html(city_url)
            if data !='0':
                print len(data)
                soup = BeautifulSoup(data,'lxml')
                shopClassList = self.shop_class(soup)
                for g in shopClassList:
                    print g[0].encode("utf8"),g[1].encode("utf8")
                time.sleep(10)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print '解析完成'
            else:
                print '网页无法打开！跳过该网页！'

if __name__ == '__main__':
    conf = {}
    for line in fileinput.input("..//..//RabbitMQ_Server.conf"):
        lines = line.replace(' ','').replace('\n','').replace('\r','').split("=")
        conf[lines[0]] = lines[1]
    shop = ShopClass()
    re = receive.Receive()
    re.receive(shop.callback,conf["USER_NAME"],conf["PWD"],conf["IP"],int(conf["PORT"]))
   # soup = shop.receive(conf["USER_NAME"],conf["PWD"],conf["IP"],int(conf["PORT"]))
