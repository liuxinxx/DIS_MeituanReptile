#encoding=utf8
from urllib import quote
import HTMLParser
import requests
from bs4 import BeautifulSoup
def downloader_html(url):##利用PhantomJS获取网页数据
    BAIDU_UA = 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html）'#百度爬虫UA
    headers = {'User-Agent': BAIDU_UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
    data = requests.get(url, headers=headers) ##这样服务器就会以为我们是真的浏览器了
    html_parser = HTMLParser.HTMLParser()
    data = html_parser.unescape(data.text)   
    return data
def fenlei(soup):##获取全国各个地区链接
    list_fenlei = []
    soup = BeautifulSoup(soup,"html.parser")    
    div_list = soup.find_all("div",class_="J-nav-item")
    for v in div_list:
        for k in v.find_all('li'):
            list =[]
            k = k.find('a')        
            fenlei_url =k.get('href')
            fenlei_name =k.get_text()
            if fenlei_url.find('dianying')==-1 or fenlei_url.find('cinemalist')!=-1:
                fenlei_url= quote(fenlei_url,'://')#对URL进行转码，防止中文造成url的打开错误
                list.append(fenlei_name)
                list.append(fenlei_url)
                list_fenlei.append(list) 
                print fenlei_name,':',fenlei_url        
    return list_fenlei
def write(str,file_name,flag):#将制定的字符串写入指定的文件中，当标记flag为1时，代表追加写入，为2时代表清除源文件后写入
    if flag == 1:
        file_object = open(file_name, 'a')
        file_object.write(str)
        file_object.close()
    if flag ==2:
        file_object = open(file_name, 'wb')
        file_object.write(str)
        file_object.close()
if __name__ == '__main__':
    CITY_URL = 'http://sz.meituan.com/'
    soup = downloader_html(CITY_URL)
    file_name = "C:\\Users\\liu\\Desktop\\data.txt"
    write(soup, file_name, 2)
    fenlei(soup)
    