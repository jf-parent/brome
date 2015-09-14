#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Assert equal and not equal'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("assert_text_test")

        ret = self.app.pdriver.assert_text_equal("id:1", "this is visible")
        assert ret

        ret = self.app.pdriver.assert_text_not_equal("id:1", "whatever")
        assert ret

        ret = self.app.pdriver.assert_text_not_equal("id:1", "this is visible")
        assert not ret

        ret = self.app.pdriver.assert_text_equal("id:1", "whatever")
        assert not ret
