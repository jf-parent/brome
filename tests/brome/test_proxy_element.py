from brome_config import default_config, default_browser_config
from model.basetest import BaseTest
from model.selector import selector_dict
from model.test_dict import test_dict
from brome.runner.local_runner import LocalRunner


def test_proxy_element_list(browser_name, brome):
    class TestProxyElementList(object):
        class Test(BaseTest):

            name = 'Proxy element list'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("proxy_element_list_test")

                divs = self.pdriver.find_all("tn:bold")

                # len
                assert len(divs) == 10

                # __getitem__
                assert divs[0].get_attribute('id') == '1'
                assert divs[1].get_attribute('id') == '2'
                assert divs[2].get_attribute('id') == '3'
                assert divs[3].get_attribute('id') == '4'
                assert divs[4].get_attribute('id') == '5'
                assert divs[5].get_attribute('id') == '6'
                assert divs[6].get_attribute('id') == '7'
                assert divs[7].get_attribute('id') == '8'
                assert divs[8].get_attribute('id') == '9'
                assert divs[9].get_attribute('id') == '10'

                # __iter__
                for i, div in enumerate(divs):
                    assert div.get_attribute('id') == '%d' % (i+1)

                # slice
                subset_divs = divs[:2]
                assert subset_divs[0].get_attribute('id') == '1'
                assert subset_divs[1].get_attribute('id') == '2'

                # slice sequence reverse
                subset_divs = divs[::-1]

                assert subset_divs[0].get_attribute('id') == '10'
                assert subset_divs[1].get_attribute('id') == '9'
                assert subset_divs[2].get_attribute('id') == '8'
                assert subset_divs[3].get_attribute('id') == '7'
                assert subset_divs[4].get_attribute('id') == '6'
                assert subset_divs[5].get_attribute('id') == '5'
                assert subset_divs[6].get_attribute('id') == '4'
                assert subset_divs[7].get_attribute('id') == '3'
                assert subset_divs[8].get_attribute('id') == '2'
                assert subset_divs[9].get_attribute('id') == '1'

                # reversed
                for i, div in enumerate(reversed(divs)):
                    assert div.get_attribute('id') != '%d' % (i+1)

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestProxyElementList]
    )
    LocalRunner(brome).execute()
