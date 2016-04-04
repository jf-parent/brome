# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import json
from datetime import datetime

import yaml
from IPython import embed

from brome.webserver import data_controller

class LaunchForm(object):
    def __init__(self, app):
        self.app = app

        self.init_data()

    def init_data(self):
        self.data = {}

        self.data['browser_list'] = data_controller.get_browser_list(self.app)

        self.data['test_list'] = data_controller.get_test_list(self.app)

    def start_test_batch(self, data):
        runner_path = os.path.join(
            self.app.brome.get_config_value('project:absolute_path'),
            self.app.brome.get_config_value("brome:brome_executable_name")
        )

        requested_browsers = [b[len("browser_"):] for b in dict(data).keys() if b.startswith("browser_")]

        if not len(requested_browsers):
            return False, 'You need to select at least one browser'

        requested_tests = [t[len("test_"):] for t in dict(data).keys() if t.startswith("test_")]

        if not len(requested_tests):
            return False, 'You need to select at least one test'

        test_file_path = os.path.join(
            self.app.temp_path,
            'test_file.yaml'
        )
        with open(test_file_path, 'w') as f:
            f.write(yaml.dump(requested_tests, default_flow_style=False))

        command = [
            sys.executable,
            runner_path,
            "run",
            "-r",
            ",".join(requested_browsers),
            "--test-file",
            test_file_path
        ]
        self.app.logger.info("Starting test bach with the following command: %s"%command)

        subprocess.Popen(
                command,
                stdout=open(os.devnull, 'w'),
                stderr=open('runner.log', 'a'),
        )

        return True, ''

class ReportForm(object):
    def __init__(self, app, object_id, object_type):
        self.app = app
        self.object_id = object_id
        self.object_type = object_type

        self.fetch_object()
        self.init_data()

    def fetch_object(self):
        if self.object_type == 'test_result':
            self.data_object = data_controller.get_test_result(self.app, self.object_id)
        elif self.object_type == 'test_crash':
            self.data_object = data_controller.get_test_crash(self.app, self.object_id)

    def init_data(self):
        self.data = {}

        #TITLE
        self.data['title'] = self.data_object.title

        #JAVASCRIPT ERROR
        try:
            self.data['javascript_error'] = json.loads(self.data_object.extra_data)['javascript_error']
        except (ValueError, KeyError):
            self.data['javascript_error'] = ''
            
        extra_data = json.loads(self.data_object.extra_data)
        #SCREENSHOT
        self.data['screenshot_path'] = self.data_object.screenshot_path
        self.data['extra_data'] = extra_data

        #NETWORK CAPTURE
        try:
            self.data['network_capture_path'] = extra_data['network_capture_path']

            if self.app.brome.get_config_value("webserver:analyse_network_capture_report_func"):
                self.data['network_capture_analyse'] = True
        except (ValueError, KeyError):
            self.data['network_capture_path'] = ''

        #VIDEO
        if self.data_object.videocapture_path != '0':
            self.data['video_path'] = self.data_object.videocapture_path
            self.data['video_title'] = self.data_object.title.replace('_', ' ')

            test_instance = data_controller.get_test_instance(self.data_object.test_instance_id)
            video_time_position = (self.data_object.timestamp - test_instance.starting_timestamp).total_seconds()
            m, s = divmod(video_time_position, 60)
            self.data['video_time_position'] =  video_time_position
            self.data['video_time_position_hr'] =  "%02d min %02d sec" % (m, s)

        #CUSTOM FIELDS
        report = self.app.brome.get_config_value("webserver:report")
        if type(report) == dict:
            self.data['custom_fields'] = report.get('custom_fields')
        else:
            self.data['custom_fields'] = None

    def report(self, data):
        self.app.logger.info("Reported!")
        
        report = self.app.brome.get_config_value("webserver:report")
        if type(report) == dict:
            on_submit = report.get('on_submit')
            module_name = on_submit.split(':')[0]
            function_name = on_submit.split(':')[1]

            module = __import__(module_name, fromlist = [''])

            success, msg = getattr(module, function_name)(dict(data))

            return success, msg
        else:
            return False, 'webserver:report:on_submit is not configured!'
