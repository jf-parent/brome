#! -*- coding: utf-8 -*-

__version__ = "0.5"

import shutil
import pickle
import hashlib
import os
import argparse
import shutil
import re
from glob import glob

import yaml

from core.model.utils import *
from core.model.meta import Session
from core.model.grep import grep_files
from core.runner.local_runner import LocalRunner
from core.runner.grid_runner import GridRunner
from core.model.meta import create_database, delete_database, setup_database, update_test
from core.model.configurator import load_brome_config, get_config_value, default_config, generate_brome_config
from webserver.app import create_app

class Brome(object):
    def __init__(self, **kwargs):
        self.config_path = kwargs.get('config_path')
        self.selector_dict = kwargs.get('selector_dict', {})
        self.test_dict = kwargs.get('test_dict', {})
        self.browsers_config_path = kwargs.get('browsers_config_path')
        self.config = load_brome_config(self.config_path)
        self.config['project']['absolute_path'] = kwargs.get('absolute_path')

        with open(self.browsers_config_path, 'r') as fd:
            self.browsers_config = yaml.load(fd)

        if not self.browsers_config:
            print 'You must provide a browsers config dict to the brome instance'
            exit(1)

    def print_usage(self):
        print 'brome_runner.py [admin | run | webserver | list | find]'
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

        #TEST SEARCH QUERY
        parser.add_argument(
                            '--search',
                            '-s',
                            dest = 'test_search_query', 
                            default = '*',
                            help = 'The search query used to activate tests'
        )
        #TEST NAME
        parser.add_argument(
                            '--name',
                            '-n',
                            dest = 'test_name', 
                            help = 'The test name to be executed'
        )

        #TEST FILE
        parser.add_argument(
            '--test-file',
            dest = 'test_file',
            default = False,
            help = 'The file containing the name of all the tests that you want to run'
        )

        #LOCALHOST RUNNER
        parser.add_argument(
                            '--localhost',
                            '-l',
                            dest = 'localhost_runner', 
                            help = 'Launch a browser from localhost'
        )

        #REMOTE RUNNER
        parser.add_argument(
                            '-r',
                            '--remote',
                            dest = 'remote_runner', 
                            default = False,
                            help = 'Launch a browser on a remote'
        )

        def test_config_string(value):
            try:
                re.match("([^=]+=[^,]+,?)+", value).group(0)
                return value
            except AttributeError:
                print "--test-config '%s' does not match required format (key=value,key1:value1)"%(value)
                exit(1)

        #TEST CONFIG KWARGS
        parser.add_argument(
                            '--test-config',
                            type = test_config_string,
                            dest = 'test_config', 
                            help = 'The config that will be pass to the test. ex: "key=value,key1=value1"'
        )

        def brome_config_string(value):
            try:
                re.match("([^:]+:[^=]+=[^,]+,?)+", value).group(0)
                return value
            except AttributeError:
                print "--brome-config '%s' does not match required format (section:key=value,section1:key1=value1)"%(value)
                exit(1)

        #BROME CONFIG KWARGS
        parser.add_argument(
                            '--brome-config',
                            type = brome_config_string,
                            dest = 'brome_config', 
                            help = 'The config that will be pass to the brome runner. ex: "section:key=value,section1:key1=value1"'
        )

        self.parsed_args = parser.parse_args(args)

        if self.test_dict:
            self.auto_update_test()

        if self.parsed_args.localhost_runner:
            browsers_id = [self.parsed_args.localhost_runner]
        elif self.parsed_args.remote_runner:
            browsers_id = self.parsed_args.remote_runner.split(',')
        else:
            print 'Please select -r or -l'
            exit(1)

        for browser_id in browsers_id:
            if browser_id not in self.browsers_config.keys():
                print 'This browser id is not available in the provided browsers config'
                print 'Supported browser(s) are: %s'%self.browsers_config.keys()
                exit(1)

        #LOCALHOST RUNNER 
        if self.parsed_args.localhost_runner:
            LocalRunner(self).execute()

        #REMOTE RUNNER
        elif self.parsed_args.remote_runner:
            GridRunner(self).execute()

        #ERROR
        else:
            print 'Select either -l "{browser_id}" or -r "{browser_id}"'

    def admin(self, args):
        parser = argparse.ArgumentParser(description='Brome admin')

        parser.add_argument(
                            '--generate-config',
                            dest = 'generate_config', 
                            action = 'store_true',
                            help = 'Generate the default brome config'
        )

        parser.add_argument(
                            '--reset',
                            dest = 'reset', 
                            action = 'store_true',
                            help = 'Reset the database + delete the test batch results + update the test table + delete all the test state'
        )

        parser.add_argument(
                            '--create-database',
                            dest = 'create_database', 
                            action = 'store_true',
                            help = 'Create the project database'
        )

        parser.add_argument(
                            '--delete-test-states',
                            dest = 'delete_test_states', 
                            action = 'store_true',
                            help = 'Delete all the test states'
        )

        parser.add_argument(
                            '--delete-test-results',
                            dest = 'delete_test_result', 
                            action = 'store_true',
                            help = 'Delete all the test batch results'
        )

        parser.add_argument(
                            '--reset-database',
                            dest = 'reset_database', 
                            action = 'store_true',
                            help = 'Reset the project database'
        )

        parser.add_argument(
                            '--delete-database',
                            dest = 'delete_database', 
                            action = 'store_true',
                            help = 'Delete the project database'
        )

        parser.add_argument(
                            '--update-test',
                            dest = 'update_test', 
                            action = 'store_true',
                            help = 'Update the test in the database'
        )

        parsed_args = parser.parse_args(args)

        def reset_database():
            delete_database(self.get_config_value('database:sqlalchemy.url'))
            create_database(self.get_config_value('database:sqlalchemy.url'))

        def delete_test_states():
            states_dir = os.path.join(
                self.get_config_value("project:absolute_path"),
                "tests",
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

            print 'States deleted'

        def delete_test_batch_result():
            if os.path.exists(self.get_config_value('project:test_batch_result_path')):
                shutil.rmtree(self.get_config_value('project:test_batch_result_path'))
                print 'Test batch result (%s) deleted!'%self.get_config_value('project:test_batch_result_path')
            else:
                print 'Nothing to delete'

        if parsed_args.create_database:
            create_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.reset:
            reset_database()
            delete_test_batch_result()
            self.update_test()
            delete_test_states()
        elif parsed_args.generate_config:
            generate_brome_config(self.config_path)
        elif parsed_args.delete_test_result:
            delete_test_batch_result()
        elif parsed_args.delete_test_states:
            delete_test_states()
        elif parsed_args.reset_database:
            delete_database(self.get_config_value('database:sqlalchemy.url'))
            create_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.delete_database:
            delete_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.update_test:
            _update_test()

    def webserver(self, args):
        app = create_app(self)
        app.run(host = self.get_config_value("webserver:HOST"), port = self.get_config_value("webserver:PORT"))

    def list_(self, args):
        query = os.path.join(
                        self.get_config_value("project:absolute_path"),
                        "tests",
                        "test_*.py"
                    )

        tests = glob(query)
        print "[index]\t|test name|"
        for index, test in enumerate(tests):
            test_name = test.split(os.sep)[-1][5:-3]
            print "[%s]\t%s"%(index, test_name)

    def find(self, args):
        parser = argparse.ArgumentParser(description='Brome find')

        parser.add_argument(
                            '--test-id',
                            dest = 'test_id', 
                            help = 'Find a test_id in model and test directory'
        )

        parser.add_argument(
                            '--selector',
                            dest = 'selector', 
                            help = 'Find a selector in model and test directory'
        )

        parsed_args = parser.parse_args(args)

        if parsed_args.test_id:
            pattern = "\.(assert_.*|create_test_result)+\(.*[\'\"]+(%s)+[\'\"]+"%parsed_args.test_id
        elif parsed_args.selector:
            pattern = "\..*\(+[\'\"]+.*(%s)+.*[\'\"]+"%parsed_args.selector

        paths = [
            os.path.join(
                self.get_config_value("project:absolute_path"),
                "tests"
            ),
            os.path.join(
                self.get_config_value("project:absolute_path"),
                "model"
            ),
        ]

        grep_files(paths, pattern, True)

    def get_config_value(self, config_name):
        config_list = [
            self.config,
            default_config
        ]
        value = get_config_value(config_list,config_name)

        return value

    def update_test(self):
        setup_database(self.get_config_value('database:*'))

        session = Session()

        if self.test_dict:
            update_test(session, self.test_dict)
        else:
            raise Exception("No test dictionary provided")

        Session.remove()
        session.close()

    def auto_update_test(self):
        old_hash = None

        brome_memory_pickle_path = os.path.join(
            self.get_config_value("project:absolute_path"),
            ".brome.pkl"
        )

        new_hash = hashlib.sha1(self.test_dict.__repr__()).hexdigest()

        if os.path.isfile(brome_memory_pickle_path): 
            with open(brome_memory_pickle_path, "rb") as fd:
                data = pickle.load(fd)

            if data.has_key('test_dict_hash'):
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
