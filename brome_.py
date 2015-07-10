#! -*- coding: utf-8 -*-

import argparse
import re

from brome.core.model.meta import Session
from brome.core.runner.local_runner import LocalRunner

class Brome(object):
    def __init__(self, **kwargs):
        self.config_path = kwargs.get('config_path')
        self.selector_dict = kwargs.get('selector_dict', {})
        self.test_dict = kwargs.get('test_dict', {})
        self.local_config_dict = kwargs.get('local_config_dict')

    def print_usage(self):
        print 'brome [generate | admin | run]'
        exit(1)

    def execute(self, args):
        if len(args) < 2:
            self.print_usage()

        if args[1] == 'run':
            self.run(args[2:])
        elif args[1] == 'generate':
            self.generate(args)
        elif args[1] == 'admin':
            self.admin(args)
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

        #LOCAL BROWSER
        parser.add_argument(
                            '--local-browser',
                            '-l',
                            dest = 'local_browser', 
                            help = 'Launch a browser from localhost'
        )

        #REMOTE BROWSER
        parser.add_argument(
                            '--remote-browser',
                            '-r',
                            dest = 'remote_browswer', 
                            help = 'Launch a browser on a remote location ("ec2", "virtualbox")'
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

        #LOCAL BROWSER
        if self.parsed_args.local_browser:
            if self.parsed_args.local_browser not in self.local_config_dict.keys():
                print 'This local browser is not supported'
                print 'Supported local browser are: %s'%self.local_config_dict.keys()
                exit(1)

            self.browser_config = self.local_config_dict
            local_runner = LocalRunner(self)
            local_runner.run()

        #EC2
        elif self.parsed_args.remote_browswer == 'ec2':
            pass

        #VIRTUALBOX
        elif self.parsed_args.remote_browswer == 'vb':
            pass

        #ERROR
        else:
            print 'Select either -r "grid" or -l "{browser_id}"'

    def generate(self, args):
        print 'generate'

    def admin(self, args):
        print 'admin'
