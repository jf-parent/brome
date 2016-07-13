#! /usr/bin/env python

from brome.webserver.server.settings import config
from brome.core.utils import delete_database

config.configure()

if config.get('ENV', 'production') != 'development':
    answer = input('Are you sure you when to delete the database?[y/N]')
else:
    answer = 'y'

if answer == 'y':
    delete_database(config.get('MONGO_DATABASE_NAME'))

print('Done')
