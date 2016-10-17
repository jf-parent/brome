
from model.nav import Nav
from model.todo import Todo
from model.basemodel import BaseModel


class App(BaseModel):
    name = 'App'
    info_format = '[{self.name}] {msg}'

    def __init__(self, pdriver, url):
        self.base_url = url
        self.pdriver = pdriver

        self.test_count = False

        self.nav = Nav(self)

    def create_todo(self, text):
        self.info('Creating todo')

        if self.test_count:
            count_before = self.get_todos_count()

        todo = Todo(self)
        todo.create(text)

        if self.test_count:
            self.pdriver.assert_text_equal(
                'sv:app_todo_count',
                str(count_before + 1),
                '#8'
            )
        return todo

    def delete_all(self):
        while True:
            el = self.pdriver.find(
                'sv:todo_root',
                raise_exception=False
            )
            if not el:
                break

            Todo(self, id=el.get_attribute('data-id')).delete()

    def clear_completed_todos(self):
        self.pdriver.find('sv:app_clear_completed_todos_btn').click()

    def set_filter(self, value):
        if value not in ['active', 'completed', 'all']:
            raise Exception('Invalid value for set_filter')

        self.info('Setting the filter...')

        self.pdriver.find('sv:app_filter_{value}'.format(value=value)).click()

    def get_todos_count(self):
        self.info('Getting todos count...')

        count_text = self.pdriver.find('sv:app_todo_count').text
        if count_text:
            count = int(count_text)
        else:
            count = 0

        self.info('Todo count: {count}'.format(count=count))
        return count

    def toggle_todos_state(self):
        self.info('Toggling todos state...')

        self.pdriver.find('sv:app_toggle_all_todos').click()
