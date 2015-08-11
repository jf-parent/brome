#! -*- coding: utf-8 -*-

import os
from glob import glob

from brome.core.model.test_batch import TestBatch
from brome.core.model.test_result import TestResult
from brome.webserver.extensions import db

def get_test_batch_list():
    data = db.session.query(TestBatch).order_by(TestBatch.id.desc()).all()

    return data

def get_test_list(app):
    data = []

    tests_dir = os.path.join(
        app.brome.get_config_value('project:absolute_path'),
        "tests"
    )

    if os.path.isdir(tests_dir):
        tests = glob(os.path.join(tests_dir, 'test_*.py'))
        for test in tests:
            name = test.split(os.sep)[-1][len('test_'):-3]
            data.append({'name': name})

    return data

def get_browser_list(app):
    data = []

    for key, browser in app.brome.browsers_config.iteritems():
        browser_config = {}
        browser_config['id'] = key
        browser_config['name'] = browser['browserName']

        icon = "fa-%s"%browser_config['name'].lower().replace(' ', '-')
        if browser_config.has_key('deviceName'):
            if 'android' in browser_config['deviceName'].lower():
                icon = "fa-android"
            elif 'iphone' in browser_config['deviceName'].lower():
                icon = "fa-mobile"
            elif 'ipad' in browser_config['deviceName'].lower():
                icon = "fa-tablet"

        browser_config['icon'] = icon

        data.append(browser_config)

    return data

def get_test_batch_screenshot(app, testbatch_id):
    data = []

    relative_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "screenshots"
    )

    abs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_dir
    )

    if os.path.isdir(abs_dir):
        for browser_dir in os.listdir(abs_dir):
            for screenshot in os.listdir(os.path.join(abs_dir, browser_dir)):
                data.append({
                    'title': screenshot.split('.')[0].replace('_', ' '),
                    'broswer_id': browser_dir.replace('_', ' '),
                    'path': os.path.join(relative_dir, browser_dir, screenshot)
                })

    return data

    

def get_test_batch_test_result(app, testbatch_id):
    data = db.session.query(TestResult)\
                .filter(TestResult.test_batch_id == testbatch_id)\
                .order_by(TestResult.result)\
                .all()

    return data

def get_test_batch_test_instance_log(app, testbatch_id, index):
    data = []

    relative_logs_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "logs"
    )

    abs_logs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_logs_dir
    )

    def ls_(dir_):
        ctime = lambda f: os.stat(os.path.join(dir_, f)).st_ctime
        return [f for f in sorted(os.listdir(dir_), key=ctime)]

    if os.path.isdir(abs_logs_dir):
        for log in ls_(abs_logs_dir):
            data.append({
                'name': log,
                'path': os.path.join(relative_logs_dir, log)
            })

    return data[index:]

def get_test_batch_crashes(app, testbatch_id):
    data = []

    relative_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "crashes"
    )

    abs_logs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_dir
    )

    if os.path.isdir(abs_logs_dir):
        crash_log_list = glob(os.path.join(abs_logs_dir, '*.log'))

        for log in crash_log_list:
            log_name = log.split(os.sep)[-1]
            file_name = ''.join(log_name.split('.')[:-1])

            with open(os.path.join(abs_logs_dir, log), 'r') as f:
                trace = f.read()
                trace = trace.split(os.linesep)

            data.append({
                'name': file_name.replace('_', ' ').title(),
                'screenshot': os.path.join(relative_dir, '%s.png'%file_name),
                'trace': trace
            })

    return data
