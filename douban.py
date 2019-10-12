# -*- coding: utf-8 -*-

import sys
import requests
import urllib
import chardet      # 编码转化处理
import traceback    # 异常处理
import random
import numpy as np
from lxml import etree

# ip池、免费IP池不好用

reload(sys)
sys.setdefaultencoding('utf8')

BaseUrl = 'https://www.kuaidaili.com/free/inha/'

class IpPool(object):
    def __init__(self):
        self.headers = [{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
                        {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
                        {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
                        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}]
        print random.choice(self.headers)

    def xpath_random(self, url):
        print('获取界面数据: {}'.format(url))
        try:
            resp = requests.get(url, headers=random.choice(self.headers), timeout=1)
            resp.encoding = chardet.detect(resp.content)['encoding']
            if resp.status_code == 200:
                print('解析提取页面href数据: {}'.format(url))
                html = etree.HTML(resp.text)
                pages = html.xpath('//div[@id="listnav"]/ul/li/a/@href')
                pages = filter(lambda x: bool(x), pages[-1].split('/'))
                pages = range(1, int(pages[-1])+1)      # 排列数组
                pages = set(random.sample(pages, k=1)) # 随机选取k个数字,去重
                pages = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                pages = map(lambda x: BaseUrl+str(x), pages)
                return self.headers, pages
            else:
                print('页面href数据提取失败: {}'.format(url))
                return [], []
        except Exception:
            print('页面数据获取失败: {}'.format(url))
            traceback.print_exc()
    
    def gethtml(self, url):
        print('正在获取页面数据: {}'.format(url))
        try:
            resp = requests.get(url, headers=random.choice(self.headers), timeout=1)
            resp.encoding = chardet.detect(resp.content)['encoding']
            proxy_list = []
            if resp.status_code == 200:
                print('解析页面数据，提取页面数据: {}'.format(url))
                html = etree.HTML(resp.text)
                trs = html.xpath('//div[@id="list"]/table/tbody/tr')
                for tr in trs:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    proto = tr.xpath('./td[4]/text()')[0].lower()
                    proxy = {proto: '{}://{}:{}'.format(proto, ip, port)}
                    proxy_list.append(proxy)
                return proxy_list
                # self.xpath_random(resp.text, url)
            else:
                print('页面数据解析失败: {}'.format(url))
                return proxy_list
        except Exception:
            print('页面数据获取失败: {}'.format(Exception))
            traceback.print_exc()

def page_get(url, header, proxie):
    print url, header, proxie
    print('获取界面数据: {}'.format(url))
    try:
        resp = requests.get(url, headers=header, proxies=proxie, timeout=1)
        resp.encoding = chardet.detect(resp.content)['encoding']
        page_list = []
        if resp.status_code == 200:
            print('获取页面数据')
            # 解析界面标签 并返回标签信息
            html = etree.HTML(resp.text)
            labels = html.xpath('//div[@class="indent tag_cloud"]/table/tbody/tr/td/a/text()')
            labels = map(lambda x:x.strip().encode('utf-8'), labels)
            return labels
        else:
            return []
    except Exception:
        print('页面数据请求失败: {}'.format(url))
        traceback.print_exc()

def book_spider(book_tag, header, proxie):
    # 传入标签 拼接url、传入headers、传入proxie
    page_num=0
    book_list=[]
    try_times=0
    # while(1):
    url='http://www.douban.com/tag/'+urllib.quote(book_tag)+'/book?start='+str(page_num*20)
    randheader=random.choice(header)
    randproxie=random.choice(proxie)
    try:
        resp = requests.get(url, headers=randheader, proxies=randproxie, timeout=1)
        resp.encoding = chardet.detect(resp.content)['encoding']
        print resp.status_code
    except Exception, ex:
        print ex
        #     page_list = []
        #     if resp.status_code == 200:
        #         print('解析页面数据')
        #         html = etree.HTML(resp.text)
        #         title = html.xpath('//div[@class="info"]/h2/a/text()')
        #         link = html.xpath('//div[@class="info"]/h2/a/@href')
        #         info = html.xpath('//div[@class="info"]/div[@class="pub"]/text()')
        #         guard = html.xpath('//div[@class="info"]/div/span[@class="rating_nums"]/text()')
        #         people = html.xpath('//div[@class="info"]/div/span[@class="pl"]/text()')
        #         desc = html.xpath('//div[@class="info"]/p/text()')
        #         print title
        #         print link
        #         print info
        #         print guard
        #         print people
        #         print desc
        #         exit(-1)
        # except Exception, ex:
        #     print ex
        #     continue

if __name__ == '__main__':
    headers, pages = IpPool().xpath_random(BaseUrl)
    proxys = []
    if pages:
        proxys = map(lambda x:IpPool().gethtml(x), pages)
        proxys = [x for y in proxys for x in y]     # 列表降维
        print proxys
    labels = page_get('https://book.douban.com/tag/?view=cloud', random.choice(headers), random.choice(proxys))
    if labels:
        for label in labels:
            book_spider(label, headers, proxys)
    # book_tag_lists = ['商业','理财','管理', '商 业','理 财','管 理']  
    # for book_tag in book_tag_lists:
    #     fun(book_tag)
