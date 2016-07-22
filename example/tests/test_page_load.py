from brome.core.basetest import BaseTest


class Test(BaseTest):

    name = 'Page load'

    def run(self, **kwargs):
        self.pdriver.get('http://localhost:7777')
        self.pdriver.assert_visible('sv:app_header', '#1')
        self.pdriver.take_screenshot('todo-page')
        self.pdriver.take_screenshot('finished-page')
