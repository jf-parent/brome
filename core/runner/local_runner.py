import copy
from datetime import datetime

from brome import *
from brome.core.runner.base_runner import BaseRunner
from brome.core.runner.local_browser import LocalBrowser

class LocalRunner(BaseRunner):
    def __init__(self, *args):
        super(LocalRunner, self).__init__(*args)

        self.browser_instances = [LocalBrowser(self, self.get_config_value("runner:local_browser"), self.browser_config)]

    def run(self):
        executed_tests = []

        tests = self.get_activated_tests()

        try:
            for test in tests:
                self.browser_instances[0].startup()

                test_instance = test.Test(browser_instance = self.browser_instances[0])
                test_instance.execute()

        except:
            raise

        finally:
            self.browser_instances[0].tear_down()
            self.terminate()

    def terminate(self):
        self.info_log('The test batch is finished.')
