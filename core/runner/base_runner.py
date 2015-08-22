#! -*- coding: utf-8 -*-

import glob
import logging
import os
import copy
import os.path
import yaml

import psutil

from brome.core.model.configurator import ini_to_dict, runner_args_to_dict, get_config_value, default_config
from brome.core.model.meta import *
from brome.core.model.test import Test
from brome.core.model.test_batch import TestBatch
from brome.core.model.test_result import TestResult
from brome.core.model.test_instance import TestInstance
from brome.core.model.utils import *

class BaseRunner(object):

    def __init__(self, brome):
        self.brome = brome
        self.brome_config_path = self.brome.config_path
        self.commandline_args = self.brome.parsed_args
        self.browsers_config = self.brome.browsers_config

        #CONFIG
        self.config = runner_args_to_dict(self.commandline_args)
        self.brome_config = self.brome.config

        setup_database(self.get_config_value('database:*'))

        self.session = Session()

        current_pid = os.getpid()

        self.tests = self.get_activated_tests()

        self.sa_test_batch = TestBatch(starting_timestamp = datetime.now())
        self.sa_test_batch.pid = current_pid
        self.sa_test_batch.total_tests = len(self.tests)
        self.session.add(self.sa_test_batch)
        self.session.commit()

        #RUNNER LOG DIR
        self.root_test_result_dir = self.get_config_value("project:test_batch_result_path")

        self.runner_dir = os.path.join(
            self.root_test_result_dir,
            "tb_%s"%self.sa_test_batch.id
        )
        self.relative_runner_dir = "tb_%s"%self.sa_test_batch.id
        create_dir_if_doesnt_exist(self.runner_dir)

        #LOGGING
        self.configure_logger()

        if self.get_config_value('runner:cache_screenshot'):
            #Dictionary that contains all the screenshot name
            self.screenshot_cache = {}

    def kill_pid(self, pid):
        try:

            p = psutil.Process(pid)

            p.terminate()

            self.info_log('Killed [pid:%s][name:%s]'%(p.pid, p.name()))
        except psutil.NoSuchProcess:
            self.error_log('No such process: [pid:%s]'%pid)

    def kill(self, procname):
        for proc in psutil.process_iter():
            if proc.name() == procname:
                self.info_log('[pid:%s][name:%s] killed'%(proc.pid, proc.name()))
                proc.kill()

    def get_available_tests(self, search_query):

        tests_path = os.path.join(
            self.get_config_value('project:absolute_path'), 
            'tests',
            'test_%s.py'%search_query
        )
        tests = sorted(glob.glob(tests_path))

        available_tests = []

        for test in tests:
            module_test = test.split(os.sep)[-1][:-3]
            available_tests.append(__import__('tests.%s'%module_test, fromlist = ['']))

        if not len(available_tests):
            self.info_log("No test found with the provided query: %s"%search_query)
        
        return available_tests

    def get_activated_tests(self):
        tests = []

        #test file
        if self.get_config_value('runner:test_file'):
            test_file_path = self.get_config_value('runner:test_file')
            with open(test_file_path, 'r') as f:
                test_list = yaml.load(f)
                for test in test_list:
                    tests.append(self.get_available_tests(test)[0])

        else:
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

        format_ = self.get_config_value("logger_runner:format")

        #Stream logger 
        if self.get_config_value('logger_runner:streamlogger'):
            sh = logging.StreamHandler()
            stream_formatter = logging.Formatter(format_)
            sh.setFormatter(stream_formatter)
            self.logger.addHandler(sh)

        #File logger
        if self.get_config_value('logger_runner:filelogger'):
            fh = logging.FileHandler(os.path.join(self.runner_dir, '%s.log'%logger_name))
            file_formatter = logging.Formatter(format_)
            fh.setFormatter(file_formatter)
            self.logger.addHandler(fh)

        self.logger.setLevel(getattr(logging, self.get_config_value('logger_runner:level')))

    def print_test_summary(self, executed_tests):
        separator = '---------------------'

        #TITLE
        self.info_log('******* TEST BATCH SUMMARY ********')

        #TOTAL NUMBER OF EXECUTED TESTS
        base_query = self.session.query(TestResult).filter(TestResult.test_batch_id == self.sa_test_batch.id)
        total_test = base_query.count()
        total_test_successful = base_query.filter(TestResult.result == True).count()
        total_test_failed = base_query.filter(TestResult.result == False).count()
        self.info_log('Total_test: %s; Total_test_successful: %s; Total_test_failed: %s'%(total_test, total_test_successful, total_test_failed))

        #EXECUTION TIME
        self.info_log("Total execution time: %s"%(self.sa_test_batch.ending_timestamp - self.sa_test_batch.starting_timestamp))

        #SEPARATOR
        self.info_log(separator)

        self.info_log('Failed tests')

        #FAILED TESTS
        failed_test_list = []
        for test_result in self.sa_test_batch.test_results:
            if not test_result.result and not test_result.test in failed_test_list:
                test = self.session.query(Test).filter(Test.id == test_result.test_id).one()
                failed_test_list.append(test_result.test)
                self.info_log("[%s] %s"%(test.test_id, test.name))

        if not failed_test_list:
            self.info_log('No test failed!')
        
        #SEPARATOR
        self.info_log(separator)

        #TEST INSTANCE REPORT
        for test in executed_tests:
            #TITLE
            self.info_log('%s %s'%(test._name, test.pdriver.get_id()))

            #TEST EXECUTION TIME
            try:
                self.info_log("Test execution time: %s"%(test._sa_test_instance.ending_timestamp - test._sa_test_instance.starting_timestamp))
            except TypeError:
                self.info_log("Test execution time exception")

            #TEST INSTANCE SUMMARY
            results = test.get_test_result_summary()
            for result in results:
                self.info_log(result)

            #CRASH REPORT
            if test._crash_error:
                self.info_log(test._crash_error)
            else:
                self.info_log('No crash!')

            #SEPARATOR
            self.info_log(separator)

        #END
        self.info_log('Finished')

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
