#!/usr/bin/env python
from distutils.core import setup

setup(
    name='django-qsstats',
    version='0.2.0',
    description='A django microframework that eases the generation of aggregate data for querysets over time.',
    author='Matt Croydon',
    author_email='mcroydon@gmail.com',
    url='http://github.com/mcroydon/django-qsstats/',
    packages=['qsstats'],
    requires=['python-dateutil'],
)
