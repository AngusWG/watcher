#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2019/4/18 17:53
# @Author  : zza
# @Email   : 740713651@qq.com
import logging
import os

import yagmail
import yaml
from flask import Flask
from flask_apscheduler import APScheduler as _BaseAPScheduler
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from watcher.browser import init_browser


class APScheduler(_BaseAPScheduler):
    """在flask下访问db"""

    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)


app = Flask(__name__)
# 读取配置
with open("local_config.yaml", "rt", encoding="utf8") as f:
    print("use {} config.yaml".format(os.path.abspath(".")))
    conf = yaml.safe_load(f)

app.config.update(conf)
db = SQLAlchemy()
redis_store = FlaskRedis(decode_responses=True)
scheduler = APScheduler()

logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)
logging.basicConfig(format=app.config["log_format"], datefmt='%Y%m%d %I:%M:%S')
logger = logging.getLogger('werkzeug')
logger.setLevel(app.config.get("LOG_LEVEL", "INFO"))


def init_app():
    """初始化"""
    print("app.root_path:{}".format(app.root_path))
    # db.init_app(app)
    redis_store.init_app(app, decode_responses=True)
    scheduler.init_app(app)
    scheduler.start()

    yagmail.register(app.config["username"], app.config["passwd"])
    app.browser = init_browser(app)

    from watcher.weibo_watcher import scheduler_init
    scheduler_init(scheduler)

    return app
