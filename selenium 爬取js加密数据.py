#coding=UTF-8

'''
 将驱动于python同路径
 1.chromedriver 下载地址：https://code.google.com/p/chromedriver/downloads/list
 2.Firefox的驱动geckodriver 下载地址：https://github.com/mozilla/geckodriver/releases/
 3.IE的驱动IEdriver 下载地址：http://www.nuget.org/packages/Selenium.WebDriver.IEDriver/
'''
import random
import json
import time
from selenium import webdriver

name_l = []
speed_l = []
user_l = []
date_l = []

url = "http://waimai.baidu.com/mobile/waimai?qt=shopcomment&shop_id=1616598411&address=%E7%A7%91%E6%8A%80%E5%88%9B%E6%96%B0%E5%9F%8E&lng=14084199.71&lat=5718168.59"
browser = webdriver.Firefox()
browser.get(url)

## 模拟触发点击选择按钮
browser.find_element_by_xpath("//div[@type='1']").click()

## 模拟人工滚动web页面
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)
browser.execute_script("var q=document.documentElement.scrollTop=1000000")
time.sleep(1)

## 获取数据
name = browser.find_elements_by_xpath("//span[@class='left']")
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

user = browser.find_elements_by_xpath("//div[@class='comment-container']")
for d in user:
    d_str = d.text.encode('unicode-escape').decode('string_escape')
    user_l.append(d.text)

	
with open("data.txt", "w") as f:
    for i in range(len(name_l)):
        data_str = "'id':'{0:d}', 'name':'{1:s}', 'date':'{2:s}', 'socre':'{3:d}', 'speed':'{4:s}', 'content':'{5:s}'".format(i, name_l[i].encode('utf8'), date_l[i], random.randint(1,5), speed_l[i].encode('utf8'), user_l[i].encode('utf8'))
        f.write(data_str)
        f.write("\n")

browser.quit()
