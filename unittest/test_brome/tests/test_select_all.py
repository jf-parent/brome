#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Select all'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("select_all_test")
        
        self.pdriver.find("id:selectme").select_all()

        self.pdriver.take_screenshot("Select-all")
