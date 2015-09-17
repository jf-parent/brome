#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Assert not present'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.go_to("assert_not_present_test")

        ret = self.pdriver.assert_not_present("id:2", wait_until_not_present = False)
        assert ret

        ret = self.pdriver.assert_not_present("id:3")
        assert not ret

        ret = self.pdriver.assert_not_present("id:3", wait_until_not_present = True)
        assert ret
