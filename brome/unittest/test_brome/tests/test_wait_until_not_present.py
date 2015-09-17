#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Wait until not present'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.go_to("wait_until_not_present_test")

        ret = self.pdriver.wait_until_not_present("id:3", raise_exception = False)
        assert ret

        ret = self.pdriver.wait_until_not_present("id:4", raise_exception = False)
        assert not False
