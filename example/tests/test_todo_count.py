from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Check Todo'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        self.app.test_count = True

        for i in range(2):
            self.app.create_todo('Test {i}'.format(i=i))

        todo = self.app.create_todo('Test 3')

        todo.check()
        todo.uncheck()
        todo.delete()

        todo = self.app.create_todo('Test 4')

        todo.check()
        todo.uncheck()
        todo.check()
        todo.delete()
