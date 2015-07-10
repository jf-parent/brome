#! -*- coding: utf-8 -*-

from brome.core.model.utils import *
from brome.core.model.meta.base import Session
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

                test_ = test.Test(
                    browser_instance = self.browser_instances[0],
                    test_batch = self.test_batch,
                    name = test.Test.name,
                    index = 1
                )
                test_.execute()

        except:
            raise

        finally:
            self.browser_instances[0].tear_down()
            self.terminate()

    def terminate(self):
        self.info_log('The test batch is finished.')

        self.test_batch.ending_timestamp = datetime.now()
        self.session.commit()
