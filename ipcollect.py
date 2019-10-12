# -*- coding: utf-8 -*-

import requests
import urllib
import urllib2
import chardet
import sys
import traceback
import json
import time
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

BaseUrl = 'https://www.kuaidaili.com/free/inha/'


class Downloader(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

    def download(self, url):
        print('正在下载页面：{}'.format(url))
        try:
            resp = requests.get(url, headers=self.headers)
            resp.encoding = chardet.detect(resp.content)['encoding']
            if resp.status_code == 200:
                # return resp.text
                # return self.xpath_page(resp.text)
                return self.xpath_msg(resp.text)
            else:
                return []
                # raise ConnectionError
        except Exception:
            print('下载页面出错：{}'.format(url))
            traceback.print_exc()

    def xpath_msg(self, resp):
        try:
            html = etree.HTML(resp)
            trs = html.xpath('//div[@id="list"]/table/tbody/tr')
            proxy_list = []
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                city = tr.xpath('./td[5]/text()')
                respts = tr.xpath('./td[6]/text()')
                ts = tr.xpath('./td[7]/text()')
                proxy = {
                    'proxy': ip + ':' + port,
                    'city': json.dumps(city),
                    'respts': json.dumps(respts),
                    'ts': json.dumps(ts)
                }
                proxy_list.append(proxy)
            return proxy_list
        except Exception:
            print('解析IP地址出错')
            traceback.print_exc()

    def xpath_page(self, resp):
        try:
            html = etree.HTML(resp)
            pages = html.xpath('//div[@id="listnav"]/ul/li/a/@href')
            pages = filter(lambda x: bool(x), pages[-1].split('/'))
            pages = range(1, int(pages[-1])+1)
            pages = map(lambda x: BaseUrl+str(x), pages)
            return pages
        except Exception, ex:
            print('page解析出错: {}'.format(ex))
            traceback.print_exc()


if __name__ == '__main__':
    pages = []
    with open('page', 'r') as fpage:
        with open('ip', 'a') as fip:
            pages = fpage.readlines()
            for page in pages:
                infos = Downloader().download(page)
                for info in infos:
                    fip.write(json.dumps(info)+'\n')
                # time.sleep(2)
                print page

    # pages = Downloader().download(BaseUrl)
    # print pages
    # with open('page', 'a') as f:
    #     for page in pages:
    #         f.write(page+'\n')



pages = ['https://www.kuaidaili.com/free/inha/1/',
         'https://www.kuaidaili.com/free/inha/2973/']

