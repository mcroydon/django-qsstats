#!/usr/bin/env python
from distutils.core import setup

setup(
    name='django-qsstats',
    version='0.3.1',
    description='A django microframework that eases the generation of aggregate data for querysets.',
    author='Matt Croydon',
    author_email='mcroydon@gmail.com',
    url='http://github.com/mcroydon/django-qsstats/',
    packages=['qsstats'],
    requires=['dateutil(>=1.4.1)'],
)
