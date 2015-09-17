#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest
from model.user import User
from model.bad_stuff import BadStuff

class Test(BaseTest):

    name = 'Register 2'

    def run(self, **kwargs):

        self.info_log("Running...")
        self.pdriver.get("http://reddit.local/")

        #self.pdriver.find(["xp://*[@class, 'test1')]", "xp://*[@class = 'test')]"])
        self.pdriver.assert_visible(["sv:test1", "xp://*[@class = 'test')]"])
