from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Filters'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        for i in range(2):
            self.app.create_todo('Test {i}'.format(i=i))

        for i in range(2):
            todo = self.app.create_todo('Test {i}'.format(i=i))
            todo.check()

        # ACTIVE
        self.app.set_filter('active')

        self.pdriver.assert_not_visible(
            'sv:app_completed_todo',
            testid='#13'
        )

        self.pdriver.assert_visible(
            'sv:app_uncompleted_todo',
            testid='#13'
        )

        # COMPLETED
        self.app.set_filter('completed')

        self.pdriver.assert_not_visible(
            'sv:app_uncompleted_todo',
            testid='#14'
        )

        self.pdriver.assert_visible(
            'sv:app_completed_todo',
            testid='#14'
        )

        # ALL
        self.app.set_filter('all')

        self.pdriver.assert_visible(
            'sv:app_completed_todo',
            testid='#15'
        )

        self.pdriver.assert_visible(
            'sv:app_uncompleted_todo',
            testid='#15'
        )
