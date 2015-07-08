#! -*- coding: utf-8 -*-

import os.path
import pickle

from brome import *
from brome.core.runner.configurator import test_config_to_dict

class BaseTest(object):

    def __init__(self, **kwargs):
        self.browser_instance = kwargs.get('browser_instance')
        self.pdriver = self.browser_instance.pdriver

        #TEST KWARGS
        self.test_config = test_config_to_dict(self.browser_instance.get_config_value("runner:test_config"))

        #LOGGING
        self.configure_logger()

    def save_state(self):
        pass

    def load_state(self):
        pass

    def configure_logger(self):
        pass

    def debug_log(self, msg):
        print '[debug_log] %s'%msg

    def info_log(self, msg):
        print '[info_log] %s'%msg

    def warning_log(self, msg):
        print '[warning_log] %s'%msg

    def error_log(self, msg):
        print '[error_log] %s'%msg

    def take_screenshot(self, name):
        pass

    def execute(self):
        try:
            self.before_run()

            self.run(**self.test_config)

            self.after_run()

        except Exception, e:
            self.error_log('Test failed')

            tb = traceback.format_exc()

            self.fail(tb)

            raise
        finally:
            self.end()

    def end(self):
        if self.browser_instance.get_config_value("runner:play_sound_on_test_finished"):
            say(self.browser_instance.get_config_value("runner:sound_on_test_finished"))

    def before_run(self):
        pass

    def after_run(self):
        pass

    def fail(self, tb):
        if self.browser_instance.get_config_value("runner:play_sound_on_test_crash"):
            say(self.browser_instance.get_config_value("runner:sound_on_test_crash"))
