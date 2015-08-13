#! -*- coding: utf-8 -*-

import os
import argparse
import shutil
import re

from brome.core.model.meta import Session
from brome.core.runner.local_runner import LocalRunner
from brome.core.runner.grid_runner import GridRunner
from brome.core.model.meta import create_database, delete_database, setup_database, update_test
from brome.core.model.configurator import ini_to_dict, get_config_value, default_config
from brome.webserver.app import create_app

class Brome(object):
    def __init__(self, **kwargs):
        self.config_path = kwargs.get('config_path')
        self.selector_dict = kwargs.get('selector_dict', {})
        self.test_dict = kwargs.get('test_dict', {})
        self.browsers_config = kwargs.get('browsers_config')
        self.config = ini_to_dict(self.config_path)
        self.config['project']['absolute_path'] = kwargs.get('absolute_path')

        if not self.browsers_config:
            print 'You must provide a browsers config dict to the brome instance'
            exit(1)

    def print_usage(self):
        print 'brome_runner.py [admin | run | webserver]'
        exit(1)

    def execute(self, args):
        if len(args) < 2:
            self.print_usage()

        if args[1] == 'run':
            self.run(args[2:])
        elif args[1] == 'generate':
            self.generate(args[2:])
        elif args[1] == 'admin':
            self.admin(args[2:])
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
                print "--brome-config '%s' does not match required format (section:key=value,section1:key1:value1)"%(value)
                exit(1)

        #BROME CONFIG KWARGS
        parser.add_argument(
                            '--brome-config',
                            type = brome_config_string,
                            dest = 'brome_config', 
                            help = 'The config that will be pass to the brome runner. ex: "section:key=value,section1:key1=value1"'
        )

        self.parsed_args = parser.parse_args(args)

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

    def generate(self, args):
        print 'generate'

    def admin(self, args):
        parser = argparse.ArgumentParser(description='Brome admin')

        parser.add_argument(
                            '--create-database',
                            dest = 'create_database', 
                            action = 'store_true',
                            help = 'Create the project database'
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

        if parsed_args.create_database:
            create_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.delete_test_result:
            if os.path.exists(self.get_config_value('project:test_batch_result_path')):
                shutil.rmtree(self.get_config_value('project:test_batch_result_path'))
                print 'Test batch result (%s) deleted!'%self.get_config_value('project:test_batch_result_path')
            else:
                print 'Nothing to delete'
        elif parsed_args.reset_database:
            delete_database(self.get_config_value('database:sqlalchemy.url'))
            create_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.delete_database:
            delete_database(self.get_config_value('database:sqlalchemy.url'))
        elif parsed_args.update_test:
            setup_database(self.get_config_value('database:*'))

            session = Session()

            if self.test_dict:
                update_test(session, self.test_dict)
            else:
                raise Exception("No test dictionary provided")

    def webserver(self, args):
        app = create_app(self)
        app.run()

    def get_config_value(self, config_name):
        config_list = [
            self.config,
            default_config
        ]
        value = get_config_value(config_list,config_name)

        return value
