#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Intercept javascript error'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to('intercept_javascript_error_test')

        #4 = "get_javascript_error return_type list return [] when there is not javascript error."
        js_error = self.pdriver.get_javascript_error(return_type = 'list')
        self.pdriver.create_test_result('#4', js_error == [])

        #5 = "get_javascript_error return_type string return $no_javascript_error_string when there is not javascript error."
        js_error = self.pdriver.get_javascript_error(return_type = 'string')
        self.pdriver.create_test_result('#5', js_error == self.pdriver.no_javascript_error_string)

        #6 = "get_javascript_error return_type list return [js_error1, js_error2] when there is javascript error."
        self.pdriver.find("id:error-btn").click()
        sleep(2)

        js_error = self.pdriver.get_javascript_error(return_type = 'list')
        self.pdriver.create_test_result('#6', len(js_error) > 0)

        #7 = "get_javascript_error return_type string return '<rc>'.join(js_error_list) when there is javascript error."
        self.pdriver.find("id:error-btn").click()
        sleep(2)

        js_error = self.pdriver.get_javascript_error(return_type = 'string')
        self.pdriver.create_test_result('#7', js_error != self.pdriver.no_javascript_error_string)
