from selenium.webdriver.common.keys import Keys

from brome.core.settings import BROME_CONFIG

from model.basemodel import BaseModel


class Todo(BaseModel):
    name = 'TODO'
    info_format = '[{self.name}-{self.id}] {msg}'

    def __init__(self, app, **kwargs):
        self.app = app
        self.pdriver = app.pdriver
        self._id = kwargs.get('id', None)
        self.completed = False

    def create(self, text):
        self.set_text(text)
        self.submit()
        self.resolve_id()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def set_text(self, value):
        self.info(
            'Setting text: {value}'.format(value=value)
        )
        self.pdriver.find('sv:app_todo_input').send_keys(value)

    def submit(self):
        self.info('Submitting...')
        self.pdriver.find('sv:app_todo_input').send_keys(Keys.ENTER)

    def delete(self):
        self.info('Deleting...')

        if self.app.test_count:
            is_completed = self.is_completed()
            count_before = self.app.get_todos_count()

        self.find().hover()
        self.find('sv:todo_delete_btn').click()

        self.pdriver.wait_until_not_present(self.get_root_xpath())

        if self.app.test_count:
            if not is_completed:
                self.pdriver.assert_text_equal(
                    'sv:app_todo_count',
                    str(count_before - 1),
                    '#10'
                )

    def edit(self, new_value):
        self.info('Editing...')

        self.find().double_click()

        self.find('sv:todo_input').send_keys(new_value, clear=True)
        self.find('sv:todo_input').send_keys(Keys.ENTER)

    def check(self):
        self.info('Checking')

        if self.app.test_count:
            count_before = self.app.get_todos_count()

        if not self.is_present('sv:todo_completed'):
            self.find("sv:todo_toggle").click()
        else:
            raise Exception(
                '[TODO] Cannot check todo because already completed'
            )

        if self.app.test_count:
            self.pdriver.assert_text_equal(
                'sv:app_todo_count',
                str(count_before - 1),
                '#9'
            )

    def uncheck(self):
        self.info('Unchecking')

        if self.app.test_count:
            count_before = self.app.get_todos_count()

        if self.is_present('sv:todo_completed'):
            self.find("sv:todo_toggle").click()
        else:
            raise Exception('[TODO] Cannot uncheck todo because not completed')

        if self.app.test_count:
            self.pdriver.assert_text_equal(
                'sv:app_todo_count',
                str(count_before + 1),
                '#11'
            )

    def toggle_check_state(self):
        self.info('Toggling check state')

        self.find("sv:todo_toggle").click()

    def get_root_xpath(self):
        return "xp://li[contains(@data-id, '{id}')]".format(id=self.id)

    def is_completed(self):
        el = self.find()
        return el.get_attribute('class') == 'completed'

    def resolve_id(self):
        self.info('Resolving id')

        js_script = "JSON.parse(window.localStorage['{storage_name}']).todos.slice(-1)[0]['id']".format(storage_name=BROME_CONFIG['project']['storage_name'])  # noqa
        self.id = self.pdriver.execute_script(
            'return {js_script}'
            .format(
                js_script=js_script
            )
        )
        if not self.id:
            raise Exception('[TODO] unable to resolve id')

        self.info(
            'Resolved id: {id}'.format(id=self.id)
        )
