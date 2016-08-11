from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Check Todo'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        todo = self.app.create_todo('Test')

        todo.check()

        todo.assert_visible("sv:todo_completed", "#2")

        raise Exception('test')
