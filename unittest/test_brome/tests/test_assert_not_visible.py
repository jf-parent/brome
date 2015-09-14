#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Assert not visible'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("assert_not_visible_test")

        ret = self.pdriver.assert_not_visible("id:2")
        assert ret

        ret = self.pdriver.assert_not_visible(
            "id:3",
            wait_until_not_visible = False
        )
        assert not ret

        ret = self.pdriver.assert_not_visible(
            "id:3",
            wait_until_not_visible = True
        )
        assert ret

        ret = self.pdriver.assert_not_visible("id:2")
        assert not ret
