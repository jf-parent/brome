#! /usr/bin/env python

import os

import yaml

from webbaseserver.utils import drop_database

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..')

brome_config_path = os.path.join(ROOT, "configs", "brome.yml")
with open(brome_config_path) as fd:
    config = yaml.load(fd)

DB_NAME = config['database']['mongo_database_name']

if config['webserver'].get('env', 'production') != 'development':
    answer = input('Are you sure you when to delete the database?[y/N]')
else:
    answer = 'y'

if answer == 'y':
    drop_database(DB_NAME)

print('Done')
