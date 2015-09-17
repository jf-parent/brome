#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

class BrowserConfig(object):
    def __init__(self, **kwargs):
        self.runner = kwargs.get('runner')
        self.browser_id = kwargs.get('browser_id')
        self.browsers_config = kwargs.get('browsers_config')

        self.config = self.browsers_config[self.browser_id]

        #LOCATION
        if self.config.has_key("amiid"):
            self.location = 'ec2'
        elif self.config.has_key("vbox_name"):
            self.location = 'virtualbox'
        elif self.config.get('appium', False):
            self.location = 'appium'
        else:
            self.location = 'localhost'

        self.validate_config()

    def validate_config(self):
        #LOCAL
        if self.location == 'localhost':
            if not 'browserName' in self.config.keys():
                msg = "Add the 'browserName' in your local_config: e.g.: 'Firefox', 'Chrome', 'Safari'"
                self.runner.critical_log(msg)
                raise Exception(msg)

        #EC2
        elif self.location == 'ec2':
            self.validate_ec2_browser_config()
        #VIRTUALBOX
        elif self.location == 'virtualbox':
            pass

    def get_id(self):
        return self.browser_id

    def get(self, key, *args):
        return self.config.get(key, *args)

    def get_platform(self):
        if self.config.has_key('platform'):
            return self.config['platform']
        elif self.config.has_key('platformName'):
            return self.config['platformName']
        else:
            msg = "Platform could not be determined from the browser config"
            self.runner.error_log(msg)
            raise Exception(msg)

    def validate_ec2_browser_config(self):
        if self.config.get('launch', True):
            required_keys = [
                'browserName',
                'platform',
                'ssh_key_path',
                'username',
                'amiid',
                'region',
                'instance_type',
                'security_group_ids',
                'selenium_command'
            ]
        else:
            required_keys = [
                'browserName',
                'platform'
            ]

        for key in required_keys:
            if not key in self.config.keys():
                msg = "Add the config: %s"%key
                self.runner.critical_log(msg)
                raise Exception(msg)

        optional_keys = {
            'terminate': True,
            'launch': True,
            'record_session': False,
            'vnc_port': 5900,
            'nb_browser_by_instance': 1,
            'max_number_of_instance': 1,
            'hub_ip': 'localhost'
        }
        for key, default in optional_keys.iteritems():
            if not key in self.config.keys():
                self.runner.warning_log("Missing config: %s; using default: %s"%(key, default))
                self.config[key] = default
