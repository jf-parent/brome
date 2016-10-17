from brome.core.stateful import Stateful


class User(Stateful):

    def __init__(self, pdriver, username):
        self.pdriver = pdriver
        self.username = username
