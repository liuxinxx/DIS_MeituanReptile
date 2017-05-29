# import socks
# import socket
# from urllib import *
# socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
# socket.socket = socks.socksocket
# print(urlopen('http://icanhazip.com').read())

#16:12B5E8962015A711601047001002329E60F966F7BD64709D0D096B364D
# -*- coding:utf-8 -*-

import os
import requests
import requesocks

url = 'https://api.ipify.org?format=json'


def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def getip_requesocks(url):
    print "(+) Sending request with requesocks..."
    session = requesocks.session()
    session.proxies = {'http': 'socks5://115.159.212.160:9051'}
    r = session.get(url)
    print "(+) IP is: " + r.text.replace("\n", "")


def main():
    print "Running tests..."
    getip_requests(url)
    getip_requesocks(url)
    os.system("""(echo authenticate '"yourpassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
    getip_requesocks(url)


if __name__ == "__main__":
    main()