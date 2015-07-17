#! -*- coding: utf-8 -*-

from brome.core.model.utils import *
from brome.core.model.configurator import validate_ec2_browser_config

class BrowserConfig(object):
    def __init__(self, **kwargs):
        self.runner = kwargs.get('runner')
        self.browser_id = kwargs.get('browser_id')
        self.runner_type = kwargs.get('runner_type')
        self.browsers_config = kwargs.get('browsers_config')

        self.config = self.browsers_config[self.browser_id]

        self.validate_browser_config()

    def validate_browser_config(self):
        #LOCAL
        if self.runner_type == 'local':
            if not 'browserName' in self.config.keys():
                raise Exception("Add the 'browserName' in your local_config: e.g.: 'Firefox', 'Chrome', 'Safari'")

        #EC2
        elif self.runner_type == 'ec2':
            self.config = validate_ec2_browser_config(self.config, self.runner)
        #VIRTUALBOX
        elif self.runner_type == 'virtualbox':
            pass

    def get(self, key):
        return self.config.get(key)
