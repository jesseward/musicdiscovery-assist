import os
from setuptools import setup

NAME = 'musicdiscovery-assist'
VERSION = '0.2.0'

setup(
    name = 'discovery_assist',
    version = VERSION,
    author = 'Jesse Ward',
    author_email = 'jesse@jesseward.com',
    description = ('A Google Assist application that provides Google Home integration with the Last.FM API.'),
    license = 'MIT',
    url = 'https://github.com/jesseward/musicdiscovery-assist',
    packages=['discovery_assist'],
    install_requires=[
        'flask>=0.12',
        'requests>=2.12.4',
        'gunicorn>=19.6.0',
        'redis>=2.10.5',
    ]
)
