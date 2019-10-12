# coding: utf-8

import random
import json
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

url = "http://waimai.baidu.com/mobile/waimai?qt=shopcomment&shop_id=1616598411&address=%E7%A7%91%E6%8A%80%E5%88%9B%E6%96%B0%E5%9F%8E&lng=14084199.71&lat=5718168.59"
browser = webdriver.PhantomJS("/srv/phantomjs/bin/phantomjs")
browser.get(url)
browser.find_element_by_xpath("//div[@type='1']").click()
# binary = FirefoxBinary('/srv/firefox')
# driver = webdriver.Firefox(firefox_binary=binary)
#driver = webdriver.Chrome()
#driver.get("http://www.baidu.com")
#driver.execute_script("var q=document.body.scrollTop=10000")

name_l = []
speed_l = []
user_l = []
date_l = []
data_l = []

name = browser.find_elements_by_class_name("left")
for d in name:
    d_str = d.text.encode('unicode-escape').decode('string_escape')
    name_l.append(d.text)

speed = browser.find_elements_by_class_name("speed")
for d in speed:
    d_str = d.text.encode('unicode-escape').decode('string_escape')
    speed_l.append(d.text)

date = browser.find_elements_by_xpath('//span[@class="right f-fr"]')
for d in date:
    d_str = d.text.encode('unicode-escape').decode('string_escape')
    date_l.append(d_str)

#user = browser.find_elements_by_class_name("comment-container")
user = browser.find_elements_by_xpath("//div[@class='comment-container']")
for d in user:
    d_str = d.text.encode('unicode-escape').decode('string_escape')
    user_l.append(d.text)

'''
with open("data.json", "w") as f:
    for i in range(len(name_l)):
        data_str = "'id':'{0:d}', 'name':'{1:s}', 'date':'{2:s}', 'socre':'{3:d}', 'speed':'{4:s}', 'content':'{5:s}'".format(i, name_l[i].encode('utf8'), date_l[i], random.randint(1,5), speed_l[i].encode('utf8'), user_l[i].encode('utf8'))
        f.write(data_str)
        f.write("\n")
'''
  
for i in range(len(name_l)):
    data_str = "'id':'{0:d}', 'name':'{1:s}', 'date':'{2:s}', 'socre':'{3:d}', 'speed':'{4:s}', 'content':'{5:s}'".format(i, name_l[i].encode('utf8'), date_l[i], random.randint(1,5), speed_l[i].encode('utf8'), user_l[i].encode('utf8'))
    print data_str
