#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Highlight'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("highlight_test")

        element = self.pdriver.find("id:1")

        element.highlight(highlight_time = 2)
