# coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import HTMLParser
import requests
import random
import os
import json
from urllib import quote
import csv
import fileinput
import codecs
from xpinyin import Pinyin


def rad_ua():  # 获取随机的浏览器UA标识
    ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    ua = random.choice(ua_list)
    return ua


def abuyun():  ##返回代理
    conf = {}
    for line in fileinput.input("..//..//abuyun.conf"):
        lines = line.replace(' ', '').replace('\n', '').split("=")
        conf[lines[0]] = lines[1]
    # 代理服务器
    proxyHost = conf["proxyHost"]
    proxyPort = conf["proxyPort"]
    # 阿布云代理隧道验证信息
    proxyUser = conf["proxyUser"]
    proxyPass = conf["proxyPass"]
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


##利用PhantomJS来加载动态网页
def downloader_html_ph(url, up_num):  ##利用PhantomJS获取网页数据
    '''
    url        :要下载的页面url
    up_num     :下拉的次数
    '''
    # print driver.service
    print '开始下拉页面加载!    URL为', url, '    下拉次数为:', up_num
    conf = {}
    for line in fileinput.input("..//..//abuyun.conf"):
        lines = line.replace(' ', '').replace('\n', '').split("=")
        conf[lines[0]] = lines[1]
    # 代理服务器
    proxyHost = conf["proxyHost"]
    proxyPort = conf["proxyPort"]
    # 阿布云代理隧道验证信息
    proxyUser = conf["proxyUser"]
    proxyPass = conf["proxyPass"]
    service_args = [
        "--proxy-type=http",
        "--proxy=%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
        },
        "--proxy-auth=%(user)s:%(pass)s" % {
            "user": proxyUser,
            "pass": proxyPass,
        },
    ]
    phantomjs_path = r"phantomjs"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 伪造浏览器UA标识，防止网站反爬虫
    ua = rad_ua()  ##获取浏览器UA
    dcap["phantomjs.page.settings.userAgent"] = ua
    # ,service_args=service_args 阿布云代理
    driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=phantomjs_path)
    driver.get(url)
    time.sleep(2)
    ##下拉浏览器页面使，页面完全加载
    dian = ''
    print '网页下拉中',
    for i in range(up_num):
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        ##进程休眠一秒等待网页加载完成
        time.sleep(2)
        dian = dian + '.'
        print '.',

    print driver.current_url, '页面获取完成，开始解析页面'

    data = driver.page_source.encode("utf-8")
    # 解决页面转义
    html_parser = HTMLParser.HTMLParser()
    data = html_parser.unescape(data)
    return data


def downloader_html(url):
    proxies = abuyun()
    UA = rad_ua()  ##从ua_list中随机取出一个字符串
    headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
    # ,proxies=proxies 阿布云代理
    data = requests.get(url, headers=headers, proxies=proxies)  ##这样服务器就会以为我们是真的浏览器了
    print data
    return data


def c_to_p(city):
    p = Pinyin()
    city = unicode(city)  # 将字符转
    pp = p.get_pinyin(chars=city, splitter='')
    return pp


def movie_info(url):
    qy = ''
    number = ''
    shop_img_url = ''
    print
    print '-------------------------------------------------------'
    print url
    proxies = abuyun()
    UA = rad_ua()  ##从ua_list中随机取出一个字符串
    headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
    data = requests.get(url, headers=headers, proxies=proxies)  ##这样服务器就会以为我们是真的浏览器了
    print data.status_code
    if data.status_code == 402:
        os._exit(0)
    # 防止ping检测过了，但是刚好网断了，造成利用本地IP访问，@~~~我的本地IP是被封的。。。。
    if data.status_code != 200:
        print '出现异常开始等待',
        #         printf_logFile('出现异常开始等待')
        while (True):
            UA = rad_ua()  ##从self.user_agent_list中随机取出一个字符串（聪明的小哥儿一定发现了这是完整的User-Agent中：后面的一半段）
            headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）
            data = requests.get(url, headers=headers, proxies=proxies)  ##这样服务器就会以为我们是真的浏览器了,proxies=proxies
            print '.',

            if data.status_code == 200:
                print
                #                 printf_logFile('异常结束！继续搞事情')
                print '异常结束！继续搞事情'
                break
            time.sleep(2)
    else:
        print '网页请求成功！', '返回代码:', data.status_code
        # #         printf_logFile('网页请求成功！'+'返回代码:'+str(data.status_code))

        soup = BeautifulSoup(data.text, "html.parser")
        qy = soup.find('a', attrs={'gaevent': 'crumb/area/1'}).get_text()  ##获取店铺区域
        # 获取联系方式
        shop_img_url = soup.find('img', attrs={'width': '250', 'height': '150'}).get('src')
        shop_number = soup.find_all('div', class_='field-group')
        number = ''
        for g in range(len(shop_number)):
            str = shop_number[g].get_text().replace(' ', '').replace("\n", '')
            if str.find('电话') != -1:  # 没找到返回-1
                number = str
                number = number[number.find('：') + 1:len(number)]
                number.replace(' ', '')
    ##返回电话和店铺图片
    return qy, number, shop_img_url


def jiexi_movie(city, mov_csv, FILE_ROOT):
    shopinfo_scvlist = []
    shopdata = []
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    print c_to_p(city)
    URL = 'https://i.meituan.com/?city=' + c_to_p(city)
    proxies = abuyun()
    start_html = requests.get(URL, headers=headers, proxies=proxies)
    soup = BeautifulSoup(start_html.text, "html.parser")
    maoyan = soup.find('a', attrs={'gaevent': 'imt/homepage/category1/99'}).get('href')
    maoyan = 'https:' + maoyan
    print maoyan
    cs = maoyan[maoyan.find('?') + 1:len(maoyan)]
    n = 0
    while (True):

        my_html = requests.get('https://m.maoyan.com/imeituan/ajax/cinema?offset=' + str(n) + '&stid_b=1&' + cs,
                               headers=headers, proxies=proxies)
        n += 20
        if len(my_html.text) < 300:
            break
        js = json.loads(my_html.text.encode('utf-8'))
        i = 0
        ti = log.LOG()
        for xx in js['cinemas']:
            shopdata = []
            shopdata.append(city)  # 店铺所在城市

            data = movie_info('http://sz.meituan.com/shop/' + str(xx['poiId']))
            shopdata.append(data[0])  # 店铺地区
            shopdata.append('电影院')  # 店铺分类
            shopdata.append(xx['nm'].encode('utf-8'))  # 店铺名字
            shopdata.append(xx['addr'].encode('utf-8'))  # 店铺地址
            shopdata.append('http://sz.meituan.com/shop/' + str(xx['poiId']))  # 店铺url
            shopdata.append(str(data[1]))  # 联系方式
            shopdata.append(str(xx['price']))  # 人均
            shopdata.append(' ')  # 店铺具体分类
            shopdata.append(data[2])  # 商家店招图片url
            if data[2].find('jpg') != -1:
                img_name = ti.whatsday() + '.jpg'
            elif data[2].find('png') != -1:
                img_name = ti.whatsday() + '.png'
            elif data[2].find('jpeg') != -1:
                img_name = ti.whatsday() + '.jpeg'
            shopdata.append(img_name)  # 图片本地名字
            print '图片本地名字：', img_name
            shopinfo_scvlist.append(shopdata)
            dow_img(data[2], img_name, city)
            i += 1
            mov_csv.writerow(shopdata)
            for key in range(len(shopdata)):
                ti.printf_logFile(str(shopdata[key]), FILE_ROOT)
                print shopdata[key]


def dow_img(img_url, img_name, city):  # 下载指定链接的图片
    FILE_ROOT = c_to_p(city)
    proxies = abuyun()
    headers = {'User-Agent': rad_ua()}
    img = requests.get(img_url, headers=headers, proxies=proxies)
    try:
        f = open(FILE_ROOT + '\\sz_shopimage\\' + img_name, 'ab')
    except Exception, e:
        os.makedirs(FILE_ROOT + '\\sz_shopimage\\')  # 创建目录
        f = open(FILE_ROOT + '\\sz_shopimage\\' + img_name, 'ab')
    f.write(img.content)
    f.close()