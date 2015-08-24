#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Wait until visible'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("wait-until-visible-test")

        #2 = "Finding element without waiting until visible should return None if that element is not visible."
        element = self.pdriver.find("id:2", wait_until_visible = False)
        if element:
            self.pdriver.create_test_result('#2', False)
        else:
            self.pdriver.create_test_result('#2', True)

        #1 = "Finding element with wait until visible should return that element if that element become visible before the timeout is reached"
        element = self.pdriver.find("id:2")
        if element:
            self.pdriver.create_test_result('#1', True)
        else:
            self.pdriver.create_test_result('#1', False)


