from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Toggle Todo State'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        todo = self.app.create_todo('Test')

        for i in range(10):
            todo.toggle_check_state()

        todo.assert_not_visible("sv:todo_completed", "#4")
