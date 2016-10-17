#! /usr/bin/env python

import os
import asyncio

import yaml

from brome.core.utils import delete_database, DbSessionContext
from brome.model.user import User

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..')

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

brome_config_path = os.path.join(ROOT, "configs", "brome.yml")
with open(brome_config_path) as fd:
    config = yaml.load(fd)

DB_NAME = config['database']['mongo_database_name']
delete_database(DB_NAME)

with DbSessionContext(DB_NAME) as session:
    # INSERT DUMMY DATA
    users = [
        {
            'name': 'test',
            'email': 'test@test.com',
            'password': '123456'
        }, {
            'name': 'to.disable',
            'email': 'to.disable@to.disable.com',
            'password': '123456'
        }, {
            'name': 'admin',
            'email': 'admin@admin.com',
            'password': '123456',
            'role': 'admin'
        }, {
            'name': 'disabled',
            'email': 'disabled@disabled.com',
            'password': '123456',
            'enable': False
        }
    ]

    for user_data in users:
        user = User()
        context = {
            'db_session': session,
            'method': 'create',
            'data': user_data
        }

        loop.run_until_complete(user.validate_and_save(context))
