import glob
import logging
import os
import copy
import os.path

import yaml
import psutil
from IPython import embed

from brome.core.configurator import runner_args_to_dict, get_config_value, default_config
from brome.model.test import Test
from brome.model.test_batch import TestBatch
from brome.model.test_instance import TestInstance
from brome.model.test_result import TestResult
from brome.core.utils import *

class BaseRunner(object):
    """Base class for the brome runner

    All brome runner inherit from this base class

    Attributes:
        brome (object)
    """

    def __init__(self, brome):
        self.brome = brome

        self.brome_config_path = self.brome.config_path
        self.commandline_args = self.brome.parsed_args
        self.browsers_config = self.brome.browsers_config

        #CONFIG
        self.config = runner_args_to_dict(self.commandline_args)
        self.brome_config = self.brome.config

        #Current pid of the runner
        current_pid = os.getpid()

        #Get the activated tests list
        self.tests = self.get_activated_tests()

        #Create test batch
        with DbSessionContext(self.get_config_value('database:mongo_database_name')) as session:
            self.starting_timestamp = datetime.now()

            test_batch = TestBatch()
            test_batch.starting_timestamp = self.starting_timestamp
            test_batch.pid = current_pid
            test_batch.total_tests = len(self.tests)

            session.save(test_batch, safe=True)

        self.test_batch_id = test_batch.get_uid()

        #RUNNER LOG DIR
        self.root_test_result_dir = self.get_config_value("project:test_batch_result_path")

        if self.root_test_result_dir:
            self.runner_dir = os.path.join(
                self.root_test_result_dir,
                "tb_%s"%self.test_batch_id
            )
            self.relative_runner_dir = "tb_%s"%self.test_batch_id
            create_dir_if_doesnt_exist(self.runner_dir)
        else:
            self.runner_dir = False

        #LOGGING
        self.configure_logger()

        #SCREENSHOT CACHE
        if self.get_config_value('runner:cache_screenshot'):
            #Dictionary that contains all the screenshot name
            self.screenshot_cache = {}

    def kill_pid(self, pid):
        """Kill process by pid

        Args:
            pid (int)
        """
        try:

            p = psutil.Process(pid)

            p.terminate()

            self.info_log('Killed [pid:%s][name:%s]'%(p.pid, p.name()))
        except psutil.NoSuchProcess:
            self.error_log('No such process: [pid:%s]'%pid)

    def kill(self, procname):
        """Kill by process name

        Args:
            procname (str)
        """
        for proc in psutil.process_iter():
            if proc.name() == procname:
                self.info_log('[pid:%s][name:%s] killed'%(proc.pid, proc.name()))
                proc.kill()

    def get_available_tests(self, search_query = None, test_name = None):
        """Return a list of all the available tests

        This function might call exit(1) if not test were found

        Returns:
            list
        """

        available_tests = []

        script_folder_name = self.get_config_value('brome:script_folder_name')
        script_test_prefix = self.get_config_value('brome:script_test_prefix')

        if search_query:

            tests_path = os.path.join(
                self.get_config_value('project:absolute_path'), 
                script_folder_name,
                '%s%s.py'%(script_test_prefix, search_query)
            )
            tests = sorted(glob.glob(tests_path))

            for test in tests:
                module_test = test.split(os.sep)[-1][:-3]
                available_tests.append(__import__('%s.%s'%(script_folder_name, module_test), fromlist = ['']))

        elif test_name:
            if test_name.endswith('.py'):
                test_name = test_name[:-3]

            try:
                available_tests.append(__import__('%s.%s'%(script_folder_name, test_name), fromlist = ['']))
            except ImportError:
                pass

        if not len(available_tests):
            query = search_query if search_query else test_name
            print("No script found with the provided query: %s"%query)
            exit(1)
        
        return available_tests

    def get_activated_tests(self):
        """Return a list of all the activated tests

        The behavior of this function is determined by the received CLI arguments

        Returns:
            list
        """
        tests = []

        #test file
        if self.get_config_value('runner:test_file'):
            test_file_path = self.get_config_value('runner:test_file')
            with open(test_file_path, 'r') as f:
                test_list = yaml.load(f)

            for test in test_list:
                tests.append(self.get_available_tests(test)[0])

        elif self.get_config_value('runner:test_name'):
            tests = self.get_available_tests(test_name = self.get_config_value('runner:test_name'))
        else:
            test_search_query = self.get_config_value('runner:test_search_query')

            #by index or slice e.g.: [0:12], [:], [0], [-1]
            if test_search_query.find('[') != -1:
                exec('tests = self.get_available_tests("*")%s'%test_search_query)

            #by name
            else:
                tests = self.get_available_tests(test_search_query)

        return tests

    def get_config_value(self, config_name):
        """Return the effective config value

        Args:
            config_name (str)

        Returns:
            value (the type vary according to the config_name)
        """

        config_list = [
            self.config,
            self.brome_config
        ]
        value = get_config_value(config_list,config_name)

        return value

    def configure_logger(self):
        """Configure the test batch runner logger
        """

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
        """Print test summary

        When the test batch is finished a test summary will be printed

        Args:
            executed_tests (list)
        """

        separator = '---------------------'

        with DbSessionContext(self.get_config_value('database:mongo_database_name')) as session:
            test_batch = session.query(TestBatch).filter(TestBatch.mongo_id == self.test_batch_id).one()

            #TITLE
            self.info_log('******* TEST BATCH SUMMARY ********')

            #TOTAL NUMBER OF EXECUTED TESTS
            base_query = session.query(TestResult).filter(TestResult.test_batch_id == self.test_batch_id)
            total_test = base_query.count()
            total_test_successful = base_query.filter(TestResult.result == True).count()
            base_query = session.query(TestResult).filter(TestResult.test_batch_id == self.test_batch_id)
            total_test_failed = base_query.filter(TestResult.result == False).count()
            self.info_log('Total_test: %s; Total_test_successful: %s; Total_test_failed: %s'%(total_test, total_test_successful, total_test_failed))

            #EXECUTION TIME
            self.info_log("Total execution time: %s"%(test_batch.ending_timestamp - test_batch.starting_timestamp))

            #SEPARATOR
            self.info_log(separator)

            self.info_log('Failed tests')

            #FAILED TESTS
            failed_test_list = []
            test_results = session.query(TestResult).filter(TestResult.test_batch_id == self.test_batch_id).all()
            for test_result in test_results:
                if not test_result.result and not test_result.test in failed_test_list:
                    query = session.query(Test).filter(Test.mongo_id == test_result.test_id)
                    if query.count():
                        test = query.one()
                        failed_test_list.append(test.test_id)
                        self.info_log("[%s] %s"%(test.test_id, test.name))
                    else:
                        failed_test_list.append(test_result.title)
                        self.info_log("[noid] %s"%(test_result.title))

            if not failed_test_list:
                self.info_log('No test failed!')
            
            #SEPARATOR
            self.info_log(separator)

            #TEST INSTANCE REPORT
            for test in executed_tests:
                #TITLE
                self.info_log('%s %s'%(test._name, test.pdriver.get_id()))

                test_instance = session.query(TestInstance).filter(TestInstance.mongo_id == test._test_instance_id).one()

                #TEST EXECUTION TIME
                try:
                    self.info_log("Test execution time: %s"%(test_instance.ending_timestamp - test_instance.starting_timestamp))
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
        return {'batchid': self.test_batch_id}

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
