from brome.core.basetest import BaseTest as BromeBaseTest
from brome.core.settings import BROME_CONFIG

from model.app import App


class BaseTest(BromeBaseTest):

    def before_run(self):
        url = BROME_CONFIG['project']['url']
        self.app = App(self.pdriver, url)
