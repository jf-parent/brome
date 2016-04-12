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

    def start_proxy(self):
        pass

    def stop_proxy(self):
        pass

    def start_video_recording(self, local_video_file_path, video_filename):
        pass

    def stop_video_recording(self):
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
