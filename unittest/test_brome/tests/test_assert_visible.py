#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Assert visible'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("wait_until_visible_test")

        ret = self.pdriver.assert_visible(
            "id:2",
            wait_until_visible = False
        )
        assert not ret

        ret = self.pdriver.assert_visible(
            "id:2",
            wait_until_visible = True
        )
        assert ret

        ret = self.pdriver.assert_visible("id:3")
        assert ret

        ret = self.pdriver.assert_visible("id:1")
        assert not ret
