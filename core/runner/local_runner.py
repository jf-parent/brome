#! -*- coding: utf-8 -*-

import traceback

from brome.core.model.utils import *
from brome.core.model.meta.base import Session
from brome.core.runner.base_runner import BaseRunner
from brome.core.runner.browser_config import BrowserConfig

class LocalRunner(BaseRunner):
    def __init__(self, *args):
        super(LocalRunner, self).__init__(*args)

        self.browser_config = BrowserConfig(
            runner = self,
            runner_type = 'local',
            browser_id = self.get_config_value("runner:local_browser"),
            browsers_config = self.brome.browsers_config
        )

        self.run()

    def run(self):
        executed_tests = []

        try:
            for test in self.tests:
                
                test_ = test.Test(
                    runner = self,
                    browser_config = self.browser_config,
                    name = test.Test.name,
                    index = 1
                )
                test_.execute()

        except:
            tb = traceback.format_exc()
            self.error_log("Exception in run of the grid runner: %s"%str(tb))
            raise

        finally:
            self.terminate()

    def terminate(self):
        self.info_log('The test batch is finished.')

        self.sa_test_batch.ending_timestamp = datetime.now()
        self.session.commit()
