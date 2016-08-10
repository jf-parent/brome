selector_dict = {}
# GENERAL
selector_dict['app_header'] = 'xp://*[contains(@class, "header")]//h1'
selector_dict['app_clear_completed_todos_btn'] = 'xp://button[contains(@class, "clear-completed")]'  # noqa
selector_dict['app_todo_count'] = 'xp://span[@class = "todo-count"]//strong'
selector_dict['app_completed_todo'] = 'xp://ul[@class="todo-list"]//li[@class = "completed"]'  # noqa
selector_dict['app_uncompleted_todo'] = 'xp://ul[@class="todo-list"]//li[not(@class = "completed")]'  # noqa
selector_dict['app_toggle_all_todos'] = 'xp://input[@class = "toggle-all"]'
selector_dict['app_filter_active'] = 'xp:(//ul[@class = "filters"]//li)[2]'
selector_dict['app_filter_completed'] = 'xp:(//ul[@class = "filters"]//li)[3]'
selector_dict['app_todo_input'] = 'xp://input[@class="new-todo"]'
selector_dict['app_filter_all'] = 'xp:(//ul[@class = "filters"]//li)[1]'
# TODO
selector_dict['todo_root'] = 'xp://li[@data-id]'
selector_dict['todo_input'] = 'xp://input[@class = "edit"]'
selector_dict['todo_toggle'] = 'xp://input[@class="toggle"]'
selector_dict['todo_completed'] = 'xp://parent::li[@class="completed"]'
selector_dict['todo_uncompleted'] = 'xp://parent::li[@class="completed"]'
selector_dict['todo_delete_btn'] = 'xp://button[@class="destroy"]'
