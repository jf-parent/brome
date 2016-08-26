from pytest import set_trace  # noqa

from brome_config import default_config, default_browser_config
from model.basetest import BaseTest
from model.selector import selector_dict
from model.test_dict import test_dict
from brome.runner.local_runner import LocalRunner


def test_local_runner(browser_name, brome):
    class TestLocalRunner(object):
        class Test(BaseTest):
            name = 'LocalRunner'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_visible_test")

                ret = self.pdriver.is_visible("id:3")
                assert ret

    brome_config = default_config.copy()
    brome_config['runner_args']['localhost_runner'] = 'phantomjs'

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestLocalRunner]
    )
    LocalRunner(brome).execute()
