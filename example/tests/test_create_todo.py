from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Create Todo'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        self.app.create_todo('Test')
