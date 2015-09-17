#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Assert present'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.go_to("assert_present_test")

        ret = self.pdriver.assert_present("id:2", wait_until_present = False)
        assert not ret

        ret = self.pdriver.assert_present("id:3")
        assert ret

        ret = self.pdriver.assert_present("id:2", wait_until_present = True)
        assert ret
