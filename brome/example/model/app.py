
from brome.core.model.stateful import Stateful

class App(Stateful):
    def __init__(self, pdriver):
        self.pdriver = pdriver
