#! /usr/bin/env python
# -*- encoding:utf-8 -*-

import subprocess
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from config import email_info
import config
import time
import os
from datetime import datetime
from siemtools import utils


# 主函数
path = "/data/wxb-data/wxb-data1"
count = 0
flag = 0
LOGGER = utils.initLogger("/data/wxb-data/wxb_data.log")
def getInfoMain():
    global count
    ls = os.listdir(path)
    count += len(ls)
    if count:
        # #发邮件
        subject = '数据同步提醒'
        content = '数据已经同步到中转服务器'
        global flag
        if flag == 1:
            now = datetime.now().strftime("%H")
            if now == config.first_time or now == config.last_time:
                LOGGER.info("data receive success, files num:{0:d}".format(count))
                send_email(email_info['SMTP_host'],email_info['from_addr'],email_info['password'],email_info['to_addrs'], subject, content)
                count = 0
        else:
            flag = 1
            LOGGER.info("data receive success, files num:{0:d}".format(count))
            send_email(email_info['SMTP_host'],email_info['from_addr'],email_info['password'],email_info['to_addrs'], subject, content)
            
    else:
        now = datetime.now().strftime("%H")
        if now == config.first_time or now == config.last_time:
            LOGGER.error("data receive failed, files num:{0:d}".format(count))
            subject = '数据同步提醒'
            content = '数据同步失败'
            send_email(email_info['SMTP_host'],email_info['from_addr'],email_info['password'],email_info['to_addrs'], subject, content)
        

def send_email(SMTP_host, from_addr, password, to_addrs, subject, content):
    email_client = SMTP(SMTP_host)
    email_client.login(from_addr, password)
    msg = MIMEText(content,'plain','utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addrs
    email_client.sendmail(from_addr, to_addrs, msg.as_string())
    email_client.quit()

if __name__ == '__main__':
    while True:
        try:
            getInfoMain()
        except Exception, e:
            print str(e)
        time.sleep(1800)
