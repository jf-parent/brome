#! -*- coding: utf-8 -*-

from selenium import webdriver

from brome.core.model.proxy_driver import ProxyDriver
from brome.core.runner.base_browser import BaseBrowser

class LocalBrowser(BaseBrowser):
    def __init__(self, runner, browser_type, local_config):
        self.browser_type = browser_type
        self.runner = runner
        self.brome = runner.brome
        self.local_config = local_config

        self.config = self.local_config[self.browser_type]

    def get_ip(self):
        return 'localhost'

    def startup(self):
        driver = getattr(webdriver, self.config['browserName'].capitalize())()
        self.pdriver = ProxyDriver(driver, self, self.runner.brome.selector_dict)
        self.pdriver.brome = self.brome

        self.configure_test_batch_dir()
        self.configure_resolution()

    def tear_down(self):
        try:
            self.pdriver.quit()
        except Exception as e:
            self.error_log('Exception driver.quit(): %s'%str(e))
