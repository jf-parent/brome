#! -*- coding: utf-8 -*-

from brome.core.model.utils import *
from brome.core.model.configurator import get_config_value, parse_brome_config_from_browser_config, default_config

class BaseBrowser(object):
    def debug_log(self, msg):
        print '[debug_log] %s'%msg

    def info_log(self, msg):
        print '[info_log] %s'%msg

    def warning_log(self, msg):
        print '[warning_log] %s'%msg

    def error_log(self, msg):
        print '[error_log] %s'%msg

    def critial_log(self, msg):
        print '[critial_log] %s'%msg

    def __repr__(self):
        return self.get_id()

    def get_id(self, join_char = '-'):
        return join_char.join([
                    self.get_browser_name(),
                    self.get_browser_version(),
                    self.get_platform()
                ])

    def get_browser_name(self):
        return self.pdriver.capabilities['browserName']

    def get_browser_version(self):
        return self.pdriver.capabilities['version'].replace('.', '_')

    def get_platform(self):
        return self.pdriver.capabilities['platform'].replace('.', '_')

    def startup(self):
        pass

    def tear_down(self):
        pass

    def get_ip_address(self):
        pass

    def get_config_value(self, config_name):
        if not hasattr(self, 'browser_brome_config'):
            self.browser_brome_config = parse_brome_config_from_browser_config(self.config)

        config_list = [
            self.browser_brome_config,
            self.runner.config,
            self.runner.brome_config,
            default_config
        ]
        value = get_config_value(config_list, config_name)

        self.debug_log("get_config_value: %s:%s"%(config_name, value))
        return value

    def configure_resolution(self):
        #Maximaze window
        if self.get_config_value('browser:maximize_window'):
            self.pdriver.maximize_window()
        else:
            #Window position
            self.pdriver.set_window_position(
                self.get_config_value('browser:window_x_position'),
                self.get_config_value('browser:window_y_position')
            )

            #Window size
            self.pdriver.set_window_size(
                self.get_config_value('browser:window_width'),
                self.get_config_value('browser:window_height')
            )

    def configure_test_batch_dir(self):
        root_test_result_dir = self.get_config_value("project:test_batch_result_path")

        #TEST BATCH DIRECTORY
        self.test_batch_dir = os.path.join(
            root_test_result_dir,
            'tb_%s'%self.runner.test_batch.id
        )
        create_dir_if_doesnt_exist(self.test_batch_dir)

        #ASSERTION SCREENSHOT DIRECTORY
        self.assertion_screenshot_dir = os.path.join(
            self.test_batch_dir,
            self.get_id(join_char = '_'),
            'assertion_screenshots/'
        )
        create_dir_if_doesnt_exist(self.assertion_screenshot_dir)

        #SCREENSHOT DIRECTORY
        self.screenshot_dir = os.path.join(
            self.test_batch_dir,
            self.get_id(join_char = '_'),
            'screenshots/'
        )
        create_dir_if_doesnt_exist(self.screenshot_dir)
