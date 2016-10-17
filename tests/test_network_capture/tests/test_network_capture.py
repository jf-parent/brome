#! -*- coding: utf-8 -*-

import requests
from brome.core.model.utils import *
from brome.core.model.basetest import BaseTest

class Test(BaseTest):

    name = 'Network Capture'

    def run(self, **kwargs):

        self.info_log("Running...")

        for i in range (20):
            self.pdriver.get("%s/request/%s"%(self.pdriver.get_config_value("project:url"), i))
