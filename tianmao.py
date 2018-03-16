#coding:utf-8

from urllib.request import Request, urlopen, quote
from urllib import error
from requests import request
from urllib.request import urlparse
import datetime, time
import lxml.html
import html
import re

def downloader(url):
    user_agent = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    headers = {'User-agent':user_agent}
    req = Request(url, headers = headers)
    try:
        html = urlopen(url).read().decode()
    except error.URLError as e:
        html = None
        if hasattr(e, 'reason'):
            print('we failed reach to a webserver')
            print(e.reason)
        if hasattr(e, 'code'):
            print('the server could not fullfill the request')
            print(e.code)

    data1 = re.findall('g_page_config = (.*?)"shopcardOff":false}};', html)    #data block
    mobilephone_list = re.findall('({"cat":"1512.*?"},)', data1[0])    #get what we want from data block
    return mobilephone_list



class Throttle:
    '''add a delay between downloads to the same domain'''
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()

'''
def downloader(url, retries):
    user_agent = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    headers = {'User-agent':user_agent}
    req = request('Get', url, headers = headers)
    try:
        html = req.text
    except error.URLError as e:
        if hasattr(e, 'reason'):
            print('we failed reach to a webserver')
            print(e.reason)
        if hasattr(e, 'code'):
            print('the server could not fullfill the request')
            print(e.code)
        #add retry times
        if retries > 0 and 500 <=e.code < 600:
            downloader(url, retries-1)
    return html

    #select info we wanted
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('.product item-1111')[0]
    #td = tree.cssselect('a.productTitle productTitle-spu')[0]
    img = td.text_content()
    return img
'''


if __name__ == '__main__':

    #results of search mobilephone in tianmao
    url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&ie=utf8'
    #print(downloader(url))
    h = downloader(url)
    #with open('/home/wangf/h.txt', 'w') as fp:
       # fp.write(html.unescape(h.decode()))

   # print(html.unescape(h.decode()))

    data1 = re.findall('g_page_config = (.*?)"shopcardOff":false}};', h)    #data block
    l = re.findall('({"cat":"1512.*?"},)', data1[0])    #get what we want from data block
    print(len(l))



