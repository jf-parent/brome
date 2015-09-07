# -*- coding: utf-8 -*-

import subprocess
import os
import sys

import yaml

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
            'bro'
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
                stdout=open(os.devnull, 'a'),
                stderr=open('runner.log', 'a'),
        )

        return True, ''
