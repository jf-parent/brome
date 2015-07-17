#! -*- coding: utf-8 -*-

import argparse
import re

from brome.core.model.meta import Session
from brome.core.runner.local_runner import LocalRunner
from brome.core.runner.grid_runner import GridRunner

class Brome(object):
    def __init__(self, **kwargs):
        self.config_path = kwargs.get('config_path')
        self.selector_dict = kwargs.get('selector_dict', {})
        self.test_dict = kwargs.get('test_dict', {})
        self.local_config_dict = kwargs.get('local_config_dict', False)
        self.ec2_config_dict = kwargs.get('ec2_config_dict', False)

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

        #EC2
        parser.add_argument(
                            '--ec2',
                            dest = 'ec2_browser', 
                            default = False,
                            help = 'Launch a browser in an ec2 instance: comma separated list of browser'
        )

        #VIRTUALBOX
        parser.add_argument(
                            '--virtualbox',
                            dest = 'virtualbox_browser', 
                            default = False,
                            help = 'Launch a browser in an virtualbox instance: comma separated list of browser'
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
            if not self.local_config_dict:
                print 'You must provide a local browser config dict to the brome instance'
                exit(1)

            if self.parsed_args.local_browser not in self.local_config_dict.keys():
                print 'This local browser is not supported'
                print 'Supported local browser(s) are: %s'%self.local_config_dict.keys()
                exit(1)

            self.browsers_config = self.local_config_dict
            local_runner = LocalRunner(self)

        #EC2
        elif self.parsed_args.ec2_browser:
            if not self.ec2_config_dict:
                print 'You must provide a ec2 browser config dict to the brome instance'
                exit(1)

            if self.parsed_args.ec2_browser not in self.ec2_config_dict.keys():
                print 'This ec2 browser is not supported'
                print 'Supported ec2 browser(s) are: %s'%self.ec2_config_dict.keys()
                exit(1)

            self.browsers_config = self.ec2_config_dict
            grid_runner = GridRunner(self)

        #VIRTUALBOX
        elif self.parsed_args.virtualbox:
            pass

        #ERROR
        else:
            print 'Select either --virtualbox "{browser_id}" or --ec2 "{browser_id}" or -l "{browser_id}"'

    def generate(self, args):
        print 'generate'

    def admin(self, args):
        print 'admin'
