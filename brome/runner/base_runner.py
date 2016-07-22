import glob
from datetime import datetime
import logging
import os
import os.path

from haikunator import Haikunator
import yaml
import psutil

from brome.core.settings import BROME_CONFIG
from brome.model.test import Test
from brome.model.testbatch import Testbatch
from brome.model.testinstance import Testinstance
from brome.model.testresult import Testresult
from brome.core.utils import (
    DbSessionContext,
    create_dir_if_doesnt_exist
)


class BaseRunner(object):
    """Base class for the brome runner

    All brome runner inherit from this base class

    Attributes:
        brome (object)
    """

    def __init__(self, brome):
        self.brome = brome
        self.log_file_path = ''

        # Current pid of the runner
        current_pid = os.getpid()

        # Get the activated tests list
        if self.brome.tests:
            if not type(self.brome.tests) == list:
                tests = [self.brome.tests]
            else:
                tests = self.brome.tests

            self.tests = tests
        else:
            self.tests = self.get_activated_tests()

        # Create test batch
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            self.starting_timestamp = datetime.now()

            haikunator = Haikunator()

            test_batch = Testbatch()
            test_batch.starting_timestamp = self.starting_timestamp
            test_batch.friendly_name = haikunator.haikunate(
                token_length=0,
                delimiter='.'
            )
            test_batch.pid = current_pid
            if BROME_CONFIG['runner_args']['remote_runner']:
                test_batch.total_tests = len(self.tests) * len(BROME_CONFIG['runner_args']['remote_runner'].split(','))  # noqa
            else:
                test_batch.total_tests = len(self.tests) * len(BROME_CONFIG['runner_args']['local_runner'].split(','))  # noqa

            session.save(test_batch, safe=True)

        self.test_batch_id = test_batch.get_uid()
        self.test_batch_friendly_name = test_batch.friendly_name

        # RUNNER LOG DIR
        self.root_test_result_dir = BROME_CONFIG["project"]["test_batch_result_path"]  # noqa

        if self.root_test_result_dir:
            self.runner_dir = os.path.join(
                self.root_test_result_dir,
                "tb_results",
                "tb_%s" % self.test_batch_id
            )
            self.relative_runner_dir = os.path.join(
                "tb_results",
                "tb_%s" % self.test_batch_id
            )
            create_dir_if_doesnt_exist(self.runner_dir)
        else:
            self.runner_dir = ''

        # LOGGING
        self.configure_logger()

        # SCREENSHOT CACHE
        if BROME_CONFIG['runner']['cache_screenshot']:
            # Dictionary that contains all the screenshot name
            self.screenshot_cache = {}

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == self.test_batch_id)\
                .one()

            test_batch.root_path = self.root_test_result_dir
            test_batch.log_file_path = self.relative_log_file_path

            session.save(test_batch, safe=True)

    def kill_pid(self, pid):
        """Kill process by pid

        Args:
            pid (int)
        """
        try:

            p = psutil.Process(pid)

            p.terminate()

            self.info_log('Killed [pid:%s][name:%s]' % (p.pid, p.name()))
        except psutil.NoSuchProcess:
            self.error_log('No such process: [pid:%s]' % pid)

    def kill(self, procname):
        """Kill by process name

        Args:
            procname (str)
        """
        for proc in psutil.process_iter():
            if proc.name() == procname:
                self.info_log(
                    '[pid:%s][name:%s] killed' %
                    (proc.pid, proc.name())
                )
                proc.kill()

    def get_available_tests(self, search_query=None, test_name=None):
        """Return a list of all the available tests

        This function might call exit(1) if not test were found

        Returns:
            list
        """

        available_tests = []

        script_folder_name = BROME_CONFIG['brome']['script_folder_name']
        script_test_prefix = BROME_CONFIG['brome']['script_test_prefix']

        if search_query:

            tests_path = os.path.join(
                BROME_CONFIG['project']['absolute_path'],
                script_folder_name,
                '%s%s.py' % (script_test_prefix, search_query)
            )
            tests = sorted(glob.glob(tests_path))

            for test in tests:
                module_test = test.split(os.sep)[-1][:-3]
                available_tests.append(
                    __import__(
                        '%s.%s' %
                        (script_folder_name, module_test),
                        fromlist=[''])
                )

        elif test_name:
            if test_name.endswith('.py'):
                test_name = test_name[:-3]

            try:
                available_tests.append(
                    __import__(
                        '%s.%s' %
                        (script_folder_name, test_name),
                        fromlist=[''])
                    )
            except ImportError:
                pass

        if not len(available_tests):
            query = search_query if search_query else test_name
            print("No script found with the provided query: %s" % query)
            exit(1)

        return available_tests

    def get_activated_tests(self):
        """Return a list of all the activated tests

        The behavior of this function is determined by
        the received CLI arguments

        Returns:
            list
        """
        tests = []

        # test file
        if BROME_CONFIG['runner_args']['test_file']:
            test_file_path = BROME_CONFIG['runner_args']['test_file']
            with open(test_file_path, 'r') as f:
                test_list = yaml.load(f)

            for test in test_list:
                tests.append(self.get_available_tests(test)[0])

        elif BROME_CONFIG['runner_args']['test_name']:
            tests = self.get_available_tests(
                test_name=BROME_CONFIG['runner_args']['test_name']
            )
        else:
            test_search_query = BROME_CONFIG['runner_args']['test_search_query']  # noqa

            # by index or slice e.g.: [0:12], [:], [0], [-1]
            if test_search_query.find('[') != -1:
                exec(
                    'tests = self.get_available_tests("*")%s' %
                    test_search_query
                )

            # by name
            else:
                tests = self.get_available_tests(test_search_query)

        return tests

    def configure_logger(self):
        """Configure the test batch runner logger
        """

        logger_name = 'brome_runner'

        self.logger = logging.getLogger(logger_name)

        format_ = BROME_CONFIG['logger_runner']['format']

        # Stream logger
        if BROME_CONFIG['logger_runner']['streamlogger']:
            sh = logging.StreamHandler()
            stream_formatter = logging.Formatter(format_)
            sh.setFormatter(stream_formatter)
            self.logger.addHandler(sh)

        # File logger
        if BROME_CONFIG['logger_runner']['filelogger'] and \
                self.runner_dir:

            self.log_file_path = os.path.join(
                    self.runner_dir,
                    '%s.log' % logger_name
            )
            self.relative_log_file_path = os.path.join(
                    self.relative_runner_dir,
                    '%s.log' % logger_name
            )

            fh = logging.FileHandler(
                self.log_file_path
            )
            file_formatter = logging.Formatter(format_)
            fh.setFormatter(file_formatter)
            self.logger.addHandler(fh)

        self.logger.setLevel(
            getattr(
                logging,
                BROME_CONFIG['logger_runner']['level']
                )
            )

    def print_test_summary(self, executed_tests):
        """Print test summary

        When the test batch is finished a test summary will be printed

        Args:
            executed_tests (list)
        """

        separator = '---------------------'

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch).filter(Testbatch.mongo_id == self.test_batch_id).one()  # noqa

            # TITLE
            self.info_log('******* TEST BATCH SUMMARY ********')

            # TOTAL NUMBER OF EXECUTED TESTS
            base_query = session.query(Testresult).filter(Testresult.test_batch_id == self.test_batch_id)  # noqa
            total_test = base_query.count()
            total_test_successful = base_query.filter(Testresult.result == True).count()  # noqa
            base_query = session.query(Testresult).filter(Testresult.test_batch_id == self.test_batch_id)  # noqa
            total_test_failed = base_query.filter(Testresult.result == False).count()  # noqa
            self.info_log(
                'Total_test: %s; Total_test_successful: %s; Total_test_failed: %s' %  # noqa
                (total_test, total_test_successful, total_test_failed)
            )

            # EXECUTION TIME
            self.info_log(
                "Total execution time: %s" %
                (test_batch.ending_timestamp - test_batch.starting_timestamp)
            )

            # SEPARATOR
            self.info_log(separator)

            self.info_log('Failed tests:')

            # FAILED TESTS
            failed_test_list = []
            test_results = session.query(Testresult)\
                .filter(Testresult.result == False)\
                .filter(Testresult.test_batch_id == self.test_batch_id).all()  # noqa
            for test_result in test_results:
                if test_result.title not in failed_test_list:
                    failed_test_list.append(test_result.title)
                    query = session.query(Test)\
                        .filter(Test.mongo_id == test_result.test_id)
                    if query.count():
                        test = query.one()
                        self.info_log(
                            "[%s] %s" %
                            (test.test_id, test.name)
                        )
                    else:
                        self.info_log(
                            "[noid] %s" %
                            (test_result.title)
                        )

            if not failed_test_list:
                self.info_log('No test failed!')

            # SEPARATOR
            self.info_log(separator)

            # TEST INSTANCE REPORT
            for test in executed_tests:
                # TITLE
                self.info_log(
                    '%s %s' %
                    (test._name, test.pdriver.get_id())
                )

                test_instance = session.query(Testinstance)\
                    .filter(Testinstance.mongo_id == test._test_instance_id)\
                    .one()

                # TEST EXECUTION TIME
                try:
                    self.info_log(
                        "Test execution time: %s" %
                        (test_instance.ending_timestamp - test_instance.starting_timestamp)  # noqa
                    )
                except TypeError:
                    self.info_log("Test execution time exception")

                # TEST INSTANCE SUMMARY
                results = test.get_test_result_summary()
                for result in results:
                    self.info_log(result)

                # CRASH REPORT
                if test._crash_error:
                    self.info_log(test._crash_error)
                else:
                    self.info_log('No crash!')

                # SEPARATOR
                self.info_log(separator)

            # END
            self.info_log('Finished')

    def get_logger_dict(self):
        return {'batchid': self.test_batch_friendly_name}

    def debug_log(self, msg):
        self.logger.debug(
            "[debug]%s" %
            msg, extra=self.get_logger_dict()
        )

    def info_log(self, msg):
        self.logger.info(
            "%s" %
            msg, extra=self.get_logger_dict()
        )

    def warning_log(self, msg):
        self.logger.warning(
            "[warning]%s" %
            msg, extra=self.get_logger_dict()
        )

    def error_log(self, msg):
        self.logger.error(
            "[error]%s" %
            msg, extra=self.get_logger_dict()
        )

    def critical_log(self, msg):
        self.logger.critical(
            "[critical]%s" %
            msg, extra=self.get_logger_dict()
        )
