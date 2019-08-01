#!/usr/bin/env python

from setuptools import setup

setup(name='target-storagegrid',
      version='0.3.0',
      description='Singer.io target for writing storagegrid files',
      author='Stitch',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['target_storagegrid'],
      install_requires=[
          'jsonschema==2.6.0',
          'singer-python==2.1.4',
      ],
      entry_points='''
          [console_scripts]
          target-storagegrid=target_storagegrid:main
      ''',
)
