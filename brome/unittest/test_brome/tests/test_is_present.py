#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Is present'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.go_to("wait_until_present_test")

        ret = self.pdriver.is_present("id:2")
        assert not ret

        ret = self.pdriver.is_present("id:3")
        assert ret
