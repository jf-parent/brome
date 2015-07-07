#! -*- coding: utf-8 -*-

from brome import *
from brome.core.model.base_test import BaseTest

class Test(BaseTest):

    name = 'Register'

    def run(self, app, **kwargs):

        app.pdriver.get("http://reddit.local/")

        sleep(3)
