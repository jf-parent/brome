from time import sleep

from brome.runner.base_instance import BaseInstance


class DummyEC2Instance(BaseInstance):

    def __init__(self, runner, browser_config, index):
        self.runner = runner
        self.browser_config = browser_config
        self.index = index

        self.private_ip = '127.0.0.%i' % self.index
        self.public_dns = 'localhost'
        self.private_dns = 'localhost'
        self.public_ip = '127.0.0.%i' % self.index

    def get_ip(self):
        return '127.0.0.1'

    def execute_command(self, command):
        sleep(1)
        return True

    def startup(self):
        sleep(1)
        return True

    def tear_down(self):
        sleep(1)
        return True

    def start_proxy(self):
        pass
        return True

    def stop_proxy(self):
        return True

    def start_video_recording(self, local_video_file_path, video_filename):
        return True

    def stop_video_recording(self):
        return True

    def debug_log(self, msg):
        print(msg)

    def info_log(self, msg):
        print(msg)

    def warning_log(self, msg):
        print(msg)

    def error_log(self, msg):
        print(msg)

    def critial_log(self, msg):
        print(msg)
