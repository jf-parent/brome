#! /usr/bin/env python

from IPython import embed
from mongoalchemy.session import Session

from brome.model.user import User
from brome.model.notification import Notification
from brome.webserver.server.settings import config

config.configure()

session = Session.connect(config.get("MONGO_DATABASE_NAME"))

q_user = session.query(User)

print('[*] q_user')

q_notification = session.query(Notification)

print('[*] q_notification')

embed()
