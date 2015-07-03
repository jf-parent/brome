class BaseBrowserInstance(object):

    def __init__(self, driver):
        self.driver = driver

    def log(self, msg):
        pass

    def get_window_position_x(self):
        pass

    def get_window_position_y(self):
        pass

    def get_window_height(self):
        pass

    def get_window_width(self):
        pass

    def __repr__(self):
        return self.get_id()

    def get_id(self):
        return '%s-%s-%s'%(
                    self.get_browser_name(),
                    self.get_browser_version(),
                    self.get_platform()
                )

    def get_browser_name(self):
        return self.driver.capabilities['browserName']

    def get_browser_version(self):
        return self.driver.capabilities['version']

    def get_platform(self):
        return self.driver.capabilities['platform']

    def startup(self):
        pass

    def tear_down(self):
        pass

    def get_ip_address(self):
        pass
