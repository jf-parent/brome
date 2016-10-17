from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Failing'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        for i in range(1, 10):
            self.pdriver.create_test_result('#%s' % i, False)
