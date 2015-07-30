#! -*- coding: utf-8 -*-

class BaseInstance(object):

    def get_ip(self):
        pass

    def execute_command(self, command):
        pass

    def startup(self):
        pass

    def tear_down(self):
        pass

    def debug_log(self, msg):
        print msg

    def info_log(self, msg):
        print msg

    def warning_log(self, msg):
        print msg

    def error_log(self, msg):
        print msg

    def critial_log(self, msg):
        print msg
