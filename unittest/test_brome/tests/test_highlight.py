#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Highlight'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.pdriver.get("%s/highlight-test"%self.pdriver.get_config_value("project:base_url"))

        element = self.pdriver.find("id:1")

        element.highlight(highlight_time = 2)
