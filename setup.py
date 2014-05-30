# -*- coding: utf-8 -*-
from setuptools import setup

import s3_proxy


setup(
  name='django-s3-proxy',
  version='.'.join(map(str, s3_proxy.__version__)),
  url='https://github.com/chillbear/django-s3-proxy',
  license='MIT',
  description='Link static apps hosted on Amazon S3 to URLs in a Django project. ',
  author='DoorDash',
  author_email='hello@doordash.com',
  packages=['s3_proxy'],
  install_requires=['requests'],
  classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Framework :: Django",
  ]
)
