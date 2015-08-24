#! -*- coding: utf-8 -*-

from brome.core.model.basetest import BaseTest as BromeBaseTest

from app import App

class BaseTest(BromeBaseTest):

    def before_run(self):
        self.app = App(self.pdriver)
