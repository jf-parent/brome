#!/usr/bin/env python

import unittest

from brome.core.models.utils import *
from brome.core.runner.local_runner import LocalRunner

class Test(unittest.TestCase):
    def test_config_value_from_brome_config(self):
        class MockArgs(object):
            pass

        mock_args = MockArgs()
        mock_args.test_search_query = '*'
        mock_args.local_browser = 'phantomjs'
        mock_args.brome_config = None

        browser_config = {}
        browser_config['phantomjs'] = {}
        browser_config['phantomjs']['browserName'] = 'PhantomJS'

        local_runner = LocalRunner("config-1.ini", mock_args, browser_config)
        assert local_runner.browser_instances[0].get_config_value('proxy_driver:default_timeout') == 10

    def test_config_value_from_browser_config(self):
        class MockArgs(object):
            pass

        mock_args = MockArgs()
        mock_args.test_search_query = '*'
        mock_args.local_browser = 'phantomjs'
        mock_args.brome_config = 'proxy_driver:default_timeout=4'

        browser_config = {}
        browser_config['phantomjs'] = {}
        browser_config['phantomjs']['browserName'] = 'PhantomJS'
        browser_config['phantomjs']['proxy_driver:default_timeout'] = 2

        local_runner = LocalRunner("config-1.ini", mock_args, browser_config)

        assert local_runner.browser_instances[0].get_config_value('proxy_driver:default_timeout') == 2

    def test_config_value_from_runner_config(self):
        class MockArgs(object):
            pass

        mock_args = MockArgs()
        mock_args.test_search_query = '*'
        mock_args.local_browser = 'phantomjs'
        mock_args.brome_config = 'proxy_driver:default_timeout=4'

        browser_config = {}
        browser_config['phantomjs'] = {}
        browser_config['phantomjs']['browserName'] = 'PhantomJS'

        local_runner = LocalRunner("config-1.ini", mock_args, browser_config)

        assert local_runner.browser_instances[0].get_config_value('proxy_driver:default_timeout') == 4

    def test_config_value_from_default_config(self):
        class MockArgs(object):
            pass

        mock_args = MockArgs()
        mock_args.test_search_query = '*'
        mock_args.local_browser = 'phantomjs'
        mock_args.brome_config = ''

        browser_config = {}
        browser_config['phantomjs'] = {}
        browser_config['phantomjs']['browserName'] = 'PhantomJS'

        local_runner = LocalRunner("config-2.ini", mock_args, browser_config)

        assert local_runner.browser_instances[0].get_config_value('proxy_driver:default_timeout') == 5

if __name__ == "__main__":
    unittest.main()
