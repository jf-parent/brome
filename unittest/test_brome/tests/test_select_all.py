#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Select all'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.pdriver.get("%s/select-all-test"%self.pdriver.get_config_value("project:base_url"))
        
        self.pdriver.find("id:selectme").select_all()

        self.pdriver.take_screenshot("Select-all")
