#!/usr/bin/env python

from setuptools import setup

setup(
    name = 'hmsearch',
    version = '0.0.1',
    license = 'MIT',
    description = 'HmSearch implementation',
    author = 'Commons Machinery',
    author_email = 'dev@commonsmachinery.se',
    keywords = 'hamming hash search mongodb',
    url = 'https://github.com/commonsmachinery/hmsearch-python',

    package_dir = { '': 'lib' },
    py_modules = [ 'hmsearch' ],

    scripts = [
        'hm_initdb.py',
        'hm_insert.py',
        'hm_lookup.py',
    ],

    install_requires = [
        'pymongo',
    ],

    setup_requires = [
        "setuptools_git",
    ],
)
