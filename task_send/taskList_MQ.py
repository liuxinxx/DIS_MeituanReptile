#encoding=utf8

import pika
import time
import HTMLParser
import fileinput
import requests
from bs4 import BeautifulSoup
from rabbitmq_queues import send
'''
获取城市列表，并添加到消息队列中
将任务添加到RabbitMQ消息队列

'''
class City(object):
    def downloader_html(self,url):##利用PhantomJS获取网页数据
        BAIDU_UA = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'#百度爬虫UA
        headers = {'User-Agent': BAIDU_UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
        data = requests.get(url, headers=headers) ##这样服务器就会以为我们是真的浏览器了,
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
           # print cityData
            city_List.append(cityData)  
        return city_List
if __name__ == '__main__':
##配置文件中读取RabbitMQ服务器的配置信息USER_NAME,PWD,IP,POST
#     USER_NAME = username
#     PWD = password
#     IP = ip115.159.212.160
#     POST = post

    conf = {}
    for line in fileinput.input("..//..//RabbitMQ_Server.conf"):
        lines = line.replace(' ','').replace('\n','').replace('\r','').split("=")
        conf[lines[0]] = lines[1]
    CITY_URL = 'http://www.meituan.com/index/changecity/initiative'
    city = City()
    soup = city.downloader_html(CITY_URL)
    message_list = city.getCityList(soup)
    #将城市队列入RabbitMQ任务队列
    send_cityInfo = send.Send()
    queue_name = 'city_task_queue'
    send_cityInfo.send(message_list,conf["USER_NAME"],conf["PWD"],conf["IP"],int(conf["PORT"]),queue_name)
    # city.send(message_list,conf["USER_NAME"],conf["PWD"],conf["IP"],int(conf["PORT"]))
  