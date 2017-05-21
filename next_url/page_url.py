#encoding=utf8
from bs4 import BeautifulSoup
'''
从队列中获取商店分类链接，
解析获取具体每一页的链接，
作为任务的具体链接,存入指定的任务队列中
'''
class Next_url():
    def next_url(self,data,city_Url):
        '''
        :param data: 
        :param city_Url: 
        :return: 
        '''
        soup = BeautifulSoup(data,"html.parser")
        try:
            nurl = soup.find('a',attrs={'gaevent':'content/page/next'}).get('href')
            nurl =nurl[nurl.find('/')+1:len(nurl)]
            nurl =nurl[nurl.find('/'):len(nurl)]
            print 'nurl:',nurl
            next_page = city_Url+nurl
            return next_page
        except:
            return '0'