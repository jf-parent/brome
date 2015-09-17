#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Find hidden'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("wait_until_visible_test")

        #DECRETATED
        #see comment proxy_driver:find_all
        """
        #2 = "Finding element with waiting until visible should return None if that element is not visible."
        element = self.pdriver.find("id:1", raise_exception = False, wait_until_visible = True, wait_until_present = False)
        if element:
            self.pdriver.create_test_result('#2', False)
        else:
            self.pdriver.create_test_result('#2', True)

        #3 = "Finding element with waiting until visible should raise Timeout exception if that element is not visible and raise_exception is set to True."
        try:
            self.pdriver.find("id:1", raise_exception = True, wait_until_visible = True, wait_until_present = False)
            self.pdriver.create_test_result('#2', False)
        except TimeoutException:
            self.pdriver.create_test_result('#2', True)
        """
