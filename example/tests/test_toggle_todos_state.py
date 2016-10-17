from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Toggle Todos State'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        for i in range(10):
            self.app.create_todo('Test {i}'.format(i=i))

        self.app.toggle_todos_state()

        self.pdriver.assert_not_visible(
            'sv:app_uncompleted_todo',
            testid='#12'
        )

        self.app.toggle_todos_state()

        self.pdriver.assert_not_visible(
            'sv:app_completed_todo',
            testid='#12'
        )
