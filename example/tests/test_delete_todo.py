from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Delete Todo'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        todo = self.app.create_todo('Test')

        todo.delete()

        todo.assert_not_visible(testid="#5")
