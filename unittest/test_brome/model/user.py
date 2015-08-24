#! -*- coding: utf-8 -*-

from brome.core.model.stateful import Stateful

class User(Stateful):

    def __init__(self, pdriver, username):
        self.pdriver = pdriver
        self.username = username
