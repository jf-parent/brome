from model.basetest import BaseTest


class Test(BaseTest):

    name = 'Edit Todo'

    def run(self, **kwargs):
        self.app.nav.go_to_home()

        todo = self.app.create_todo('Old Value')
        self.app.create_todo('Test')

        todo.edit('New Value')

        self.pdriver.assert_visible(
            'xp://label[contains(text(), "New Value")]',
            '#16'
        )
        self.pdriver.assert_not_visible(
            'xp://label[contains(text(), "Old Value")]',
            '#16'
        )
