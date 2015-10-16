#! -*- coding: utf-8 -*-

import traceback

from brome.core.model.utils import *
from brome.core.model.meta.base import Session
from brome.core.runner.localhost_instance import LocalhostInstance
from brome.core.runner.base_runner import BaseRunner
from brome.core.runner.browser_config import BrowserConfig
from brome.core.model.test_batch import TestBatch

class LocalRunner(BaseRunner):
    def __init__(self, *args):
        super(LocalRunner, self).__init__(*args)

    def execute(self):
        self.browser_config = BrowserConfig(
            runner = self,
            browser_id = self.get_config_value("runner:localhost_runner"),
            browsers_config = self.brome.browsers_config
        )

        try:
            self.run()
        except KeyboardInterrupt:
            self.info_log("Test batch interrupted")

        except:
            tb = traceback.format_exc()
            self.error_log("Exception in run of the grid runner: %s"%str(tb))
            raise
        
        finally:
            self.terminate()

    def run(self):
        self.info_log("The test batch is ready.")

        self.executed_tests = []

        for test in self.tests:
            
            localhost_instance = LocalhostInstance(
                runner = self,
                browser_config = self.browser_config,
                test_name = test.Test.name
            )

            localhost_instance.startup()

            test_ = test.Test(
                runner = self,
                browser_config = self.browser_config,
                name = test.Test.name,
                test_batch_id = self.test_batch_id,
                localhost_instance = localhost_instance,
                index = 1
            )

            test_.execute()
            self.executed_tests.append(test_)

            localhost_instance.tear_down()

    def terminate(self):

        self.info_log('The test batch is finished.')

        session = Session()
        sa_test_batch = Session.query(TestBatch).filter(TestBatch.id == self.test_batch_id).one()
        sa_test_batch.ending_timestamp = datetime.now()
        session.commit()
        session.close()

        self.print_test_summary(self.executed_tests)
