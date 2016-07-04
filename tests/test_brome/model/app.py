#! -*- coding: utf-8 -*-

class App(object):
    def __init__(self, pdriver):
        self.pdriver = pdriver

    def go_to(self, page):
        self.pdriver.get("%s/%s"%(self.pdriver.get_config_value("project:url"), page))
