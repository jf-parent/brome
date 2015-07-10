#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Register'

    def run(self, **kwargs):
        self.pdriver.get("http://reddit.local/")

        self.pdriver.take_screenshot()
        self.pdriver.take_screenshot('test')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#3')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#2')
        self.pdriver.assert_visible("xp://*[@class = 'test')]", '#2')
        self.pdriver.assert_visible("xp://*[@class = 'test')]", '#1')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#1')
        self.pdriver.find_all("xp://*[@class = 'test')]")

        sleep(3)
