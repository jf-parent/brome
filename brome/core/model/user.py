#! -*- coding: utf-8 -*-

from flask_login import UserMixin

from brome.core.model.utils import *
from brome.webserver.extensions import bcrypt
from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, Text, Boolean

class User(SurrogatePK, UserMixin, Base):

    username = Column(Text())
    email = Column(Text())
    password = Column(Text())
    created_at = Column(DateTime())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
