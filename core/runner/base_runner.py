import glob
import logging
import os
import copy
import os.path
from IPython import embed

from brome.core.runner.configurator import ini_to_dict, runner_args_to_dict, get_config_value, default_config

class BaseRunner(object):

    def __init__(self, brome):
        self.brome = brome
        self.brome_config_path = self.brome.config_path
        self.commandline_args = self.brome.parsed_args
        self.browser_config = self.brome.browser_config

        #CONFIG
        self.config = runner_args_to_dict(self.commandline_args)
        self.brome_config = ini_to_dict(self.brome_config_path)

        if self.get_config_value('runner:cache_screenshot'):
            #Dictionary that contains all the screenshot name
            self.screenshot_cache = {}

    def get_available_tests(self, search_query):

        tests_path = os.path.join(self.get_config_value('project:absolute_path'), ('tests/test_%s.py'%search_query))
        tests = sorted(glob.glob(tests_path))

        available_tests = []

        for test in tests:
            module_test = test.split(os.sep)[-1][:-3]
            available_tests.append(__import__('tests.%s'%module_test, fromlist = ['']))
        
        return available_tests

    def get_activated_tests(self):
        test_search_query = self.get_config_value('runner:test_search_query')

        #by index slice eg: [0:12], [:], [0], [-1]
        if test_search_query.find('[') != -1:
            exec('tests = self.get_available_tests("*")%s'%test_search_query)

        #by name
        else:
            tests = self.get_available_tests(test_search_query)

        return tests

    def get_config_value(self, config_name):
        config_list = [
            self.config,
            self.brome_config,
            default_config
        ]
        value = get_config_value(config_list,config_name)

        return value

    def debug_log(self, msg):
        print '[debug_log] %s'%msg

    def info_log(self, msg):
        print '[info_log] %s'%msg

    def warning_log(self, msg):
        print '[warning_log] %s'%msg

    def error_log(self, msg):
        print '[error_log] %s'%msg

    def critial_log(self, msg):
        print '[critial_log] %s'%msg
