#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2019/4/29 17:57
# @Author  : zza
# @Email   : 740713651@qq.com

from os.path import dirname, join

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup
)

with open(join(dirname(__file__), 'watcher/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

ext_modules = [
]

setup(
    name='watcher',
    version=version,
    description='watcher',
    packages=find_packages(exclude=[]),
    author='AngusWG',
    author_email='',
    license='Apache License v2',
    package_data={'': ['*.*']},
    install_requires=[str(ir.req) for ir in parse_requirements("requirements.txt", session=False)],
    ext_modules=ext_modules,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "watcher = watcher.manager:cli"
        ]
    },
)
