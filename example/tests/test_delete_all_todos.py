from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Delete All Todos'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        for i in range(20):
            self.app.create_todo('Test {i}'.format(i=i))

        self.app.delete_all()

        self.pdriver.assert_not_visible('sv:todo_root', '#6')
