#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Wait until not visible'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("wait_until_not_visible_test")

        self.pdriver.wait_until_not_visible("id:2", raise_exception = False)

        element = self.pdriver.find("id:2", raise_exception = False)

        assert element == None
