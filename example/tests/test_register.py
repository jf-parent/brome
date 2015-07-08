#! -*- coding: utf-8 -*-

from brome import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Register'

    def run(self, **kwargs):

        self.pdriver.get("http://reddit.local/")

        sleep(3)
