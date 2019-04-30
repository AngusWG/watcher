#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2019/4/29 18:22
# @Author  : zza
# @Email   : 740713651@qq.com

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def init_browser(app):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) " \
                                                "AppleWebKit/537.36 (KHTML, like Gecko) " \
                                                "Chrome/63.0.3239.26 Safari/537.36 Core/" \
                                                "1.63.6716.400 QQBrowser/10.2.2214.40"
    dcap["phantomjs.page.settings.loadImages"] = True
    browser = webdriver.PhantomJS(app.config["phantomjs"],
                                  service_args=service_args,
                                  desired_capabilities=dcap)
    return browser
