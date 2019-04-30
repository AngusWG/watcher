#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2018/8/19 15:01 
# @author  : zza
# @Email   : 740713651@qq.com
import os
import time

import requests
import yagmail
from flask import current_app

from watcher.extensions import logger, app, redis_store


def scheduler_init(scheduler):
    @scheduler.task('interval', id='hour_job', **app.config.get('SCHEDULER_CONFIG'))
    def loading_redis_data_job():
        # ubuntu 中文乱码问题
        # https://blog.csdn.net/sinat_21302587/article/details/53585527
        # sudo apt-get install xfonts-wqy
        with app.app_context():
            for user_id in current_app.config["user_id"]:
                made_png(user_id)
            send_email()
            logger.info("一次扫描完成")


def send_email():
    png_list = [file for file in os.listdir(".") if file.endswith(".png")]
    if len(png_list) == 0:
        logger.info("没有更新")
        return False
    yag = yagmail.SMTP(current_app.config["username"], current_app.config["passwd"], host='smtp.qq.com')
    yag.send(to='740713651@qq.com', subject='微博更新通知 v2.0',
             contents=[yagmail.inline(image_path) for image_path in png_list])
    [os.remove(file) for file in png_list]
    return True


def made_png(user_id):
    logger.info("start {}".format(user_id))
    elements = get_elements(user_id)
    texts = [i.text for i in elements if not redis_store.hexists(user_id, i.text)]
    logger.info("获得最近{}条记录".format(len(texts)))
    if len(texts) == 0:
        return False

    file_name = "{}_{}.png".format(str(user_id), str(int(time.time())))
    time.sleep(3)
    current_app.browser.save_screenshot(file_name)
    [redis_store.hset(user_id, text, "True") for text in texts]
    logger.info("{}扫描完成".format(user_id))
    return True


def get_elements(user_id):
    while True:
        proxy = requests.get("{}/get/".format(current_app.config["proxy_url"])).content
        proxy1 = proxy.decode().split(":")
        try:
            current_app.browser.command_executor._commands['executePhantomScript'] = (
                'POST', '/session/$sessionId/phantom/execute')
            command = {'script': '''phantom.setProxy({},{},{});'''.format(proxy1[0], proxy1[1], "http"),
                       'args': []}
            current_app.browser.execute('executePhantomScript', command)
            current_app.browser.get('https://m.weibo.com/u/{}'.format(user_id))
            current_app.browser.implicitly_wait(10)
            elements = current_app.browser.find_elements_by_xpath('//div[@class="weibo-text"]')
            return elements
        except Exception:
            requests.get("{}/delete/?proxy={}".format(current_app.config["proxy_url"], proxy))
            continue
