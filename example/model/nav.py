class Nav(object):

    def __init__(self, app):
        self.app = app
        self.pdriver = app.pdriver

    def go_to_home(self):
        self.pdriver.get(self.app.base_url)

        self.pdriver.take_screenshot('Home')
