from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Clear All Completed Todos'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        completed_todos = []
        for i in range(10):
            todo = self.app.create_todo('Test {i}'.format(i=i))
            todo.check()
            completed_todos.append(todo)

        remaining_todos = []
        for i in range(10, 20):
            todo = self.app.create_todo('Test {i}'.format(i=i))
            remaining_todos.append(todo)

        self.app.clear_completed_todos()

        for todo in completed_todos:
            todo.assert_not_visible(testid='#7')

        for todo in remaining_todos:
            todo.assert_visible(testid='#7')
