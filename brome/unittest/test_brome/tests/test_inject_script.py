#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Inject script'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("select_all_test")

        try:
            self.pdriver.execute_script("return module_test.test;")
            self.pdriver.create_test_result("Inject script unittest", False)
        except WebDriverException:
            self.pdriver.create_test_result("Inject script unittest", True)

        self.pdriver.inject_js_script("/static/test_script.js")

        ret = self.pdriver.execute_script("return module_test.test;")
        self.pdriver.create_test_result("Inject script unittest", ret == "test")
