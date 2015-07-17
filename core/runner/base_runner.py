#! -*- coding: utf-8 -*-

import glob
import logging
import os
import copy
import os.path

from brome.core.model.configurator import ini_to_dict, runner_args_to_dict, get_config_value, default_config
from brome.core.model.meta import *
from brome.core.model.test_batch import TestBatch
from brome.core.model.utils import *

class BaseRunner(object):

    def __init__(self, brome):
        self.brome = brome
        self.brome_config_path = self.brome.config_path
        self.commandline_args = self.brome.parsed_args
        self.browsers_config = self.brome.browsers_config

        #CONFIG
        self.config = runner_args_to_dict(self.commandline_args)
        self.brome_config = ini_to_dict(self.brome_config_path)

        delete_database(self.get_config_value('database:sqlalchemy.url'), 'brome_example')
        create_database(self.get_config_value('database:sqlalchemy.url'), 'brome_example')
        
        setup_database(self.get_config_value('database:*'))

        self.session = Session()

        #Update the test dict
        if self.brome.test_dict:
            update_test(self.session, self.brome.test_dict)

        self.sa_test_batch = TestBatch(starting_timestamp = datetime.now())
        self.session.add(self.sa_test_batch)
        self.session.commit()

        #RUNNER LOG DIR
        self.root_test_result_dir = self.get_config_value("project:test_batch_result_path")

        self.runner_dir = os.path.join(
            self.root_test_result_dir,
            "tb_%s"%self.sa_test_batch.id
        )
        create_dir_if_doesnt_exist(self.runner_dir)

        #LOGGING
        self.configure_logger()

        if self.get_config_value('runner:cache_screenshot'):
            #Dictionary that contains all the screenshot name
            self.screenshot_cache = {}

        self.tests = self.get_activated_tests()

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

    def configure_logger(self):
        logger_name = 'brome_runner'

        self.logger = logging.getLogger(logger_name)

        format_ = "[%(batchid)s]%(message)s"

        #Stream logger 
        if self.get_config_value('logger_runner:streamlogger'):
            sh = logging.StreamHandler()
            stream_formatter = logging.Formatter(format_)
            sh.setFormatter(stream_formatter)
            self.logger.addHandler(sh)

        #File logger
        if self.get_config_value('logger_runner:filelogger'):
            fh = logging.FileHandler('%s/%s.log'%(self.runner_dir, logger_name))
            file_formatter = logging.Formatter(format_)
            fh.setFormatter(file_formatter)
            self.logger.addHandler(fh)

        self.logger.setLevel(getattr(logging, self.get_config_value('logger_runner:level')))

    def get_logger_dict(self):
        return {'batchid': self.sa_test_batch.id}

    def debug_log(self, msg):
        self.logger.debug("[debug]%s"%msg, extra=self.get_logger_dict())

    def info_log(self, msg):
        self.logger.info("%s"%msg, extra=self.get_logger_dict())

    def warning_log(self, msg):
        self.logger.warning("[warning]%s"%msg, extra=self.get_logger_dict())

    def error_log(self, msg):
        self.logger.error("[error]%s"%msg, extra=self.get_logger_dict())

    def critical_log(self, msg):
        self.logger.critical("[critical]%s"%msg, extra=self.get_logger_dict())
