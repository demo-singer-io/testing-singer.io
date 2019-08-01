#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-webscraper',
      version='1.0.0',
      description='Singer.io tap for extracting data from the webscraper ',
      author='Munish',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_webscraper'],
      install_requires=[
          'singer-python==5.3.3',
          'requests==2.20.0'
      ],
      entry_points='''
          [console_scripts]
          tap-webscraper=tap_webscraper:main
      ''',
      packages=['tap_webscraper'],
      package_data = {
          'tap_webscraper': ['tap_webscraper/*.json']
      },
      include_package_data=True
)
