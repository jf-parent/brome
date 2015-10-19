#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

class BrowserConfig(object):
    """Class that hold the effective browser config

    Attributes:
        runner (object)
        browser_id (str)
        browsers_config (dict)
    """
    def __init__(self, runner, browser_id, browsers_config):
        self.runner = runner
        self.browser_id = browser_id
        self.browsers_config = browsers_config

        #Get the effective browser config
        self.config = self.browsers_config[self.browser_id]

        #LOCATION
        if self.config.get("amiid"):
            self.location = 'ec2'

        elif self.config.get("vbname"):
            self.location = 'virtualbox'

        elif self.config.get('appium'):
            self.location = 'appium'

        elif self.config.get('saucelabs'):
            self.location = 'saucelabs'

        elif self.config.get('browserstack'):
            self.location = 'browserstack'

        else:
            self.location = 'localhost'

        #Validation
        self.validate_config()

    def validate_config(self):
        """Validate that the browser config contains all the needed config
        """

        #LOCALHOST
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
            self.validate_virtualbox_config()

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
        """Validate that the ec2 config is conform
        """

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

    def validate_virtualbox_config(self):
        """Validate that the virtualbox config is conform
        """
        if self.config.get('launch', True):
            required_keys = [
                'browserName',
                'platform',
                'username',
                'password',
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
            'vbox_type': 'gui',
            'vnc_port': 5900,
            'nb_browser_by_instance': 1,
            'max_number_of_instance': 1,
            'hub_ip': 'localhost'
        }
        for key, default in optional_keys.iteritems():
            if not key in self.config.keys():
                self.runner.warning_log("Missing config: %s; using default: %s"%(key, default))
                self.config[key] = default
