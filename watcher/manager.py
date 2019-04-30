#!/usr/bin/python3
# encoding: utf-8 
# @Time    : 2019/4/23 14:22
# @Author  : zza
# @Email   : 740713651@qq.com
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from watcher.extensions import init_app, redis_store, db

app = init_app()
manager = Manager(app)


def make_shell_context():
    return dict(
        redis_store=redis_store,
        db=db)


@manager.command
def init():
    db.create_all()
    return True


def cli():
    manager.run()


def run(**kwargs):
    args = dict(host='127.0.0.1', port=5373)
    args.update(kwargs)
    app.run(**args)


manager.add_command("shell", Shell(use_ipython=True, make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    run()
