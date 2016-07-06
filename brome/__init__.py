#! -*- coding: utf-8 -*-

import webbrowser
import shutil
import pickle
import hashlib
import os
import argparse
import re
from glob import glob

from brome.core.utils import (
    update_test,
    DbSessionContext,
    delete_database
)
from brome.core.grep import grep_files
from brome.webserver.server.app import run_app
from brome.runner.local_runner import LocalRunner
from brome.runner.grid_runner import GridRunner
from brome.core.configurator import (
    save_brome_config,
    get_config_value,
    generate_brome_config
)

__version__ = "1.0.0"


class Brome(object):
    def __init__(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, **kwargs):
        self.config = kwargs.get('config', generate_brome_config())
        self.selector_dict = kwargs.get('selector_dict', {})
        self.test_dict = kwargs.get('test_dict', {})
        self.browsers_config = kwargs.get('browsers_config', {})
        self.tests = kwargs.get('tests', [])

        if 'project' in self.config:
            absolute_path = kwargs.get('absolute_path')
            self.config['project']['absolute_path'] = absolute_path
            if not absolute_path:
                print('[Warning] absolute_path not provided in the brome.configure()')  # noqa

    def print_usage(self):
        print('$ ./bro admin | run | webserver | list | find')
        exit(1)

    def execute(self, args):
        if len(args) < 2:
            self.print_usage()

        if args[1] == 'run':
            self.run(args[2:])
        elif args[1] == 'admin':
            self.admin(args[2:])
        elif args[1] == 'find':
            self.find(args[2:])
        elif args[1] == 'list':
            self.list_(args[2:])
        elif args[1] == 'webserver':
            self.webserver(args[2:])
        else:
            self.print_usage()

    def run(self, args):
        parser = argparse.ArgumentParser(description='Brome runner')

        # TEST SEARCH QUERY
        parser.add_argument(
                            '--search',
                            '-s',
                            dest='test_search_query',
                            default='*',
                            help='The search query used to activate tests'
        )
        # TEST NAME
        parser.add_argument(
                            '--name',
                            '-n',
                            dest='test_name',
                            help='The test name to be executed'
        )

        # TEST FILE
        parser.add_argument(
            '--test-file',
            dest='test_file',
            default=False,
            help='The file containing the tests name'
        )

        # LOCALHOST RUNNER
        parser.add_argument(
                            '--localhost',
                            '-l',
                            dest='localhost_runner',
                            help='Launch a browser from localhost'
        )

        # REMOTE RUNNER
        parser.add_argument(
                            '-r',
                            '--remote',
                            dest='remote_runner',
                            default=False,
                            help='Launch a browser on a remote'
        )

        def test_config_string(value):
            try:
                re.match("([^=]+=[^,]+,?)+", value).group(0)
                return value
            except AttributeError:
                print("--test-config '%s' does not match required format (key=value,key1:value1)" % (value))  # noqa
                exit(1)

        # TEST CONFIG KWARGS
        parser.add_argument(
                            '--test-config',
                            type=test_config_string,
                            dest='test_config',
                            help='The config that will be pass to the test. ex: "key=value,key1=value1"'  # noqa
        )

        def brome_config_string(value):
            try:
                re.match("([^:]+:[^=]+=[^,]+,?)+", value).group(0)
                return value
            except AttributeError:
                print("--brome-config '%s' does not match required format (section:key=value,section1:key1=value1)" % (value))  # noqa
                exit(1)

        # BROME CONFIG KWARGS
        parser.add_argument(
                            '--brome-config',
                            type=brome_config_string,
                            dest='brome_config',
                            help='The config that will be pass to the brome runner. ex: "section:key=value,section1:key1=value1"'  # noqa
        )

        self.parsed_args = parser.parse_args(args)

        if self.test_dict:
            self.auto_update_test()

        if self.parsed_args.localhost_runner:
            browsers_id = [self.parsed_args.localhost_runner]
        elif self.parsed_args.remote_runner:
            browsers_id = self.parsed_args.remote_runner.split(',')
        else:
            print('Please select -r or -l')
            exit(1)

        for browser_id in browsers_id:
            if browser_id not in self.browsers_config.keys():
                print('This browser id is not available in the provided browsers config')  # noqa
                print('Supported browser(s) are: %s' % self.browsers_config.keys())  # noqa
                exit(1)

        # LOCALHOST RUNNER
        if self.parsed_args.localhost_runner:
            LocalRunner(self).execute()

        # REMOTE RUNNER
        elif self.parsed_args.remote_runner:
            GridRunner(self).execute()

        # ERROR
        else:
            print('Select either -l "{browser_id}" or -r "{browser_id}"')

    def admin(self, args):
        parser = argparse.ArgumentParser(description='Brome admin')

        parser.add_argument(
                            '--generate-config',
                            dest='generate_config',
                            action='store_true',
                            help='Generate the default brome config'
        )

        parser.add_argument(
                            '--reset',
                            dest='reset',
                            action='store_true',
                            help='Reset the database + delete the test batch results + update the test table'  # noqa
        )

        parser.add_argument(
                            '--delete-test-states',
                            dest='delete_test_states',
                            action='store_true',
                            help='Delete all the test states'
        )

        parser.add_argument(
                            '--delete-test-results',
                            dest='delete_test_result',
                            action='store_true',
                            help='Delete all the test batch results'
        )

        parser.add_argument(
                            '--reset-database',
                            dest='reset_database',
                            action='store_true',
                            help='Reset the project database'
        )

        parser.add_argument(
                            '--delete-database',
                            dest='delete_database',
                            action='store_true',
                            help='Delete the project database'
        )

        parser.add_argument(
                            '--update-test',
                            dest='update_test',
                            action='store_true',
                            help='Update the test in the database'
        )

        parsed_args = parser.parse_args(args)

        def reset_database():
            delete_database(
                self.get_config_value('database:mongo_database_name')
            )

        def delete_test_states():
            states_dir = os.path.join(
                self.get_config_value("project:absolute_path"),
                self.get_config_value("brome:script_folder_name"),
                "states"
            )
            try:
                shutil.rmtree(states_dir)
            except OSError:
                pass

            try:
                os.makedirs(states_dir)
            except OSError:
                pass

            print('States deleted')

        def delete_test_batch_result():
            test_batch_result_path = self.get_config_value(
                'project:test_batch_result_path'
            )
            if os.path.exists(test_batch_result_path):
                shutil.rmtree(test_batch_result_path)
                print(
                    'Test batch result (%s) deleted!'
                    % self.get_config_value('project:test_batch_result_path')
                )
            else:
                print('Nothing to delete')

        if parsed_args.reset:
            reset_database()
            delete_test_batch_result()
            if self.test_dict:
                self.update_test()
        elif parsed_args.generate_config:
            output_path = "./brome.yml"
            config = generate_brome_config()
            save_brome_config(output_path, config)
        elif parsed_args.delete_test_result:
            delete_test_batch_result()
        elif parsed_args.delete_test_states:
            delete_test_states()
        elif parsed_args.reset_database:
            delete_database(
                self.get_config_value('database:mongo_database_name')
            )
        elif parsed_args.delete_database:
            delete_database(
                self.get_config_value('database:mongo_database_name')
            )
        elif parsed_args.update_test:
            self.update_test()

    def open_browser(self):
        if self.get_config_value("webserver:open_browser"):
            webbrowser.open(
                "http://%s:%s/tb/list" %
                (
                    self.get_config_value("webserver:HOST"),
                    self.get_config_value("webserver:PORT")
                )
            )

    def webserver(self, args):
        self.config['webserver']['MONGO_DATABASE_NAME'] = self.config['database']['mongo_database_name']  # noqa
        self.config['webserver']['MONGO_HOST'] = self.config['database']['mongo_host']  # noqa
        run_app(self.config['webserver'])

    def list_(self, args):
        query = os.path.join(
                        self.get_config_value("project:absolute_path"),
                        self.get_config_value("brome:script_folder_name"),
                        "%s*.py" %
                        self.get_config_value('brome:script_test_prefix')
                    )

        tests = glob(query)
        print("[index]\t|test name|")
        for index, test in enumerate(tests):
            test_name = test.split(os.sep)[-1][5:-3]
            print("[%s]\t%s" % (index, test_name))

    def find(self, args):
        parser = argparse.ArgumentParser(description='Brome find')

        parser.add_argument(
                            '--test-id',
                            dest='test_id',
                            help='Find a test_id in model and test directory'
        )

        parser.add_argument(
                            '--unused-test-id',
                            dest='unused_test_id',
                            action='store_true',
                            help='Find all unused test id in model and test directory'  # noqa
        )

        parser.add_argument(
                            '--selector',
                            dest='selector',
                            help='Find a selector in model and test directory'
        )

        parser.add_argument(
                            '--unused-selector',
                            dest='unused_selector',
                            action='store_true',
                            help='Find all unused selector variable in model and test directory'  # noqa
        )

        parsed_args = parser.parse_args(args)

        test_id_regex = "[\'\"]+(%s){1}[\'\"]+"
        selector_regex = "\..*\(+[\'\"]+.*(%s)+.*[\'\"]+"
        if parsed_args.test_id:
            pattern = test_id_regex % parsed_args.test_id
        elif parsed_args.selector:
            pattern = selector_regex % parsed_args.selector

        paths = [
            os.path.join(
                self.get_config_value("project:absolute_path"),
                self.get_config_value("brome:script_folder_name")
            ),
            os.path.join(
                self.get_config_value("project:absolute_path"),
                "model"
            ),
        ]

        if parsed_args.test_id or parsed_args.selector:
            result = grep_files(paths, pattern, True)
        else:
            if parsed_args.unused_selector:
                print('Unused selector variable:')
                dict_ = self.selector_dict
                regex_ = selector_regex

            elif parsed_args.unused_test_id:
                print('Unused test id:')
                dict_ = self.test_dict
                regex_ = test_id_regex

            try:
                for key in dict_:
                    pattern = regex_ % key
                    result = grep_files(paths, pattern, True, return_list=True)
                    if not result:
                        print(key)

            except KeyboardInterrupt:
                pass

    def get_config_value(self, config_name):
        config_list = [
            self.config
        ]
        value = get_config_value(config_list, config_name)

        return value

    def update_test(self):
            if self.test_dict:
                with DbSessionContext(self.get_config_value('database:mongo_database_name')) as session:  # noqa
                    update_test(session, self.test_dict)
            else:
                raise Exception("No test dictionary provided")

    def auto_update_test(self):
        brome_memory_pickle_path = os.path.join(
            self.get_config_value("project:absolute_path"),
            ".brome.pkl"
        )

        new_hash = hashlib.sha1(
            self.test_dict.__repr__().encode('utf')
            ).hexdigest()

        if os.path.isfile(brome_memory_pickle_path):
            with open(brome_memory_pickle_path, "rb") as fd:
                data = pickle.load(fd)

            if 'test_dict_hash' in data:
                if data['test_dict_hash'] != new_hash:
                    self.update_test()

                    data['test_dict_hash'] = new_hash
                    with open(brome_memory_pickle_path, "wb") as fd:
                        pickle.dump(data, fd)
        else:
            data = {}
            data['test_dict_hash'] = new_hash

            with open(brome_memory_pickle_path, "wb") as fd:
                pickle.dump(data, fd)
