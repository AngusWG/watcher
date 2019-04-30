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
    dcap["phantomjs.page.settings.userAgent"] = app.config["user_agent"]
    dcap["phantomjs.page.settings.loadImages"] = True
    browser = webdriver.PhantomJS(app.config["phantomjs"],
                                  service_args=service_args,
                                  desired_capabilities=dcap)
    return browser
