
from brome.core.runner.configurator import get_config_value, parse_brome_config_from_browser_config, default_config

class BaseBrowser(object):
    def debug_log(self, msg):
        print '[debug_log] %s'%msg

    def info_log(self, msg):
        print '[info_log] %s'%msg

    def warning_log(self, msg):
        print '[warning_log] %s'%msg

    def error_log(self, msg):
        print '[error_log] %s'%msg

    def critial_log(self, msg):
        print '[critial_log] %s'%msg

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

    def get_config_value(self, config_name):
        if not hasattr(self, 'browser_brome_config'):
            self.browser_brome_config = parse_brome_config_from_browser_config(self.config)

        config_list = [
            self.browser_brome_config,
            self.runner.config,
            self.runner.brome_config,
            default_config
        ]
        value = get_config_value(config_list, config_name)

        return value
