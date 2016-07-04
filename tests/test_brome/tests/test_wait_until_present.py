#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Wait until present'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.go_to("wait_until_present_test")

        el = self.pdriver.wait_until_present("id:3")
        assert el.get_attribute('id') == '3'

        el = self.pdriver.wait_until_present("id:1", raise_exception = False, timeout = 6)
        assert el.get_attribute('id') == '1'

        el = self.pdriver.wait_until_present("id:2", raise_exception = False)
        assert not el

        el = self.pdriver.wait_until_present("id:2", raise_exception = False, timeout = 11)
        assert el.get_attribute('id') == '2'

