#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Is visible'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("wait_until_visible_test")

        ret = self.pdriver.is_visible("id:3")
        assert ret

        ret = self.pdriver.is_visible("id:1")
        assert not ret
