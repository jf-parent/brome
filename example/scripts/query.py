#! /usr/bin/env python

import os

import yaml
from IPython import embed
from mongoalchemy.session import Session

from webbaseserver.model.user import User
from webbaseserver.model.notification import Notification

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..')

brome_config_path = os.path.join(ROOT, "configs", "brome.yml")
with open(brome_config_path) as fd:
    config = yaml.load(fd)

DB_NAME = config['database']['mongo_database_name']

session = Session.connect(DB_NAME)

q_user = session.query(User)

print('[*] q_user')

q_notification = session.query(Notification)

print('[*] q_notification')

embed()
