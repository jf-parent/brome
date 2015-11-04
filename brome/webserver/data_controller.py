#! -*- coding: utf-8 -*-

import os
from glob import glob
import shutil
import psutil
from datetime import datetime
import json

from IPython import embed
from brome.core.model.test_batch import TestBatch
from brome.core.model.test_instance import TestInstance
from brome.core.model.test_result import TestResult
from brome.core.model.test_crash import TestCrash
from brome.core.model.test import Test
from brome.webserver.extensions import db

def analyse_network_capture(app, network_capture_path, analyse_function):
    network_capture_path = os.path.join(app.brome.get_config_value('project:test_batch_result_path'), network_capture_path)

    analyse_network_capture_func = app.brome.get_config_value("webserver:%s"%analyse_function)
    module_name = analyse_network_capture_func.split(':')[0]
    function_name = analyse_network_capture_func.split(':')[1]

    module = __import__(module_name, fromlist = [''])
    data = getattr(module, function_name)(network_capture_path)
    
    return data

def get_network_capture(app, testbatch_id):
    data = []

    relative_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "network_data"
    )

    abs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_dir
    )

    if os.path.isdir(abs_dir):
        for f in os.listdir(abs_dir):
            network_capture = {}
            network_capture['name'] = f.split('.')[0]
            network_capture['path'] = os.path.join(relative_dir, f)
            analyse = app.brome.get_config_value("webserver:analyse_network_capture_func")
            if analyse:
                network_capture['analyse'] = analyse

            data.append(network_capture)

    return data

def get_test_batch_list():
    data = db.session.query(TestBatch).order_by(TestBatch.id.desc()).all()

    return data

def get_active_test_instance(app, testbatch_id):
    test_instances = db.session.query(TestInstance)\
                            .filter(TestInstance.test_batch_id == testbatch_id)\
                            .filter(TestInstance.ending_timestamp == None)\
                            .all()

    for test_instance in test_instances:
        extra_data = json.loads(test_instance.extra_data)
        if extra_data.has_key('instance_public_ip'):
            test_instance.public_ip = extra_data['instance_public_ip']
        else:
            test_instance.public_ip = False

    return test_instances

def get_total_execution_time(app, testbatch_id):
    test_batch = get_test_batch(testbatch_id)

    if test_batch.ending_timestamp:
        total_execution_time = test_batch.ending_timestamp - test_batch.starting_timestamp
    else:
        total_execution_time = 'still running...'

    return total_execution_time

def get_test_batch_result_dir(app, testbatch_id):
    return os.path.join(
        app.brome.get_config_value("project:test_batch_result_path"),
        'tb_%s'%testbatch_id
    )

def delete_test_batch(app, testbatch_id):
    test_batch = get_test_batch(testbatch_id)

    db.session.delete(test_batch)
    db.session.commit()

    shutil.rmtree(get_test_batch_result_dir(app, testbatch_id))

def stop_test_batch(app, testbatch_id):
    test_batch = get_test_batch(testbatch_id)

    test_batch.killed = True
    ret = psutil.pid_exists(test_batch.pid)
    if not ret and test_batch.ending_timestamp is None:
        test_batch.ending_timestamp = datetime.now()

    db.session.commit()

def get_test_batch(testbatch_id):
    data = db.session.query(TestBatch).filter(TestBatch.id == testbatch_id).one()

    return data

def get_test_batch_detail(app, testbatch_id):
    data = db.session.query(TestBatch).filter(TestBatch.id == testbatch_id).one()

    data.total_crashes = get_total_crashes(app, testbatch_id)
    data.total_executing_tests = get_total_executing_tests(testbatch_id)
    data.total_finished_tests = get_total_finished_tests(testbatch_id)
    data.total_tests = get_total_tests(testbatch_id)
    data.total_screenshots = get_test_batch_screenshot(app, testbatch_id, only_total = True)
    data.total_test_results = get_test_batch_test_result(app, testbatch_id, only_total = True)
    data.total_failed_tests = get_test_batch_test_result(app, testbatch_id, only_failed_total = True)
    data.total_execution_time = get_total_execution_time(app, testbatch_id)

    return data

def get_total_tests(testbatch_id):
    return get_test_batch(testbatch_id).total_tests

def get_total_crashes(app, testbatch_id):
    relative_logs_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "crashes"
    )

    abs_logs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_logs_dir
    )

    return len(glob(os.path.join(abs_logs_dir, '*.log')))

def get_total_finished_tests(testbatch_id):
    count = db.session.query(TestInstance)\
        .filter(TestInstance.test_batch_id == testbatch_id)\
        .filter(TestInstance.ending_timestamp != None)\
        .count()

    return count

def get_total_executing_tests(testbatch_id):
    count = db.session.query(TestInstance)\
        .filter(TestInstance.test_batch_id == testbatch_id)\
        .filter(TestInstance.ending_timestamp == None)\
        .count()

    return count

def get_test_list(app):
    data = []

    tests_dir = os.path.join(
        app.brome.get_config_value('project:absolute_path'),
        "tests"
    )

    if os.path.isdir(tests_dir):
        tests = glob(os.path.join(tests_dir, 'test_*.py'))
        for test in sorted(tests):
            name = test.split(os.sep)[-1][len('test_'):-3]
            data.append({'name': name})

    return data

def get_browser_list(app):
    data = []

    for key, browser in app.brome.browsers_config.iteritems():
        if browser.get('available_in_webserver', False):
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

def get_test_batch_screenshot(app, testbatch_id, only_total = False):
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
            screenshot_list = os.listdir(os.path.join(abs_dir, browser_dir))

            for screenshot in screenshot_list:
                data.append({
                    'title': screenshot.split('.')[0].replace('_', ' '),
                    'browser_id': browser_dir.replace('_', ' '),
                    'path': os.path.join(relative_dir, browser_dir, screenshot)
                })

    if only_total:
        return len(data)

    return data

def get_test_result(app, test_result_id):
    return db.session.query(TestResult)\
                .filter(TestResult.id == test_result_id)\
                .one()

def get_test_crash(app, test_crash_id):
    return db.session.query(TestCrash)\
                .filter(TestCrash.id == test_crash_id)\
                .one()

def get_test_batch_test_result(app, testbatch_id, only_total = False, only_failed_total = False):
    query_ = db.session.query(TestResult)\
                .filter(TestResult.test_batch_id == testbatch_id)

    if only_total:
        return query_.count()
    elif only_failed_total:
        return query_.filter(TestResult.result == False).count()
    else:
        query_ = query_.join(Test, TestResult.test_id == Test.id)
        return query_.order_by(TestResult.result, Test.test_id).all()

def get_test_batch_log(app, testbatch_id):
    abs_logs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        "tb_%s"%testbatch_id
    )

    runner_log = []
    log_path = os.path.join(abs_logs_dir, "brome_runner.log")
    if os.path.isfile(log_path):
        with open(log_path, 'r') as f:
            runner_log = f.read().replace('"', '&quot;').replace("'", '&quot;').splitlines()

    return runner_log

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
        """
        ctime = lambda f: os.stat(os.path.join(dir_, f)).st_ctime
        return [f for f in sorted(os.listdir(dir_), key=ctime)]
        """
        return [f for f in os.listdir(dir_)]

    if os.path.isdir(abs_logs_dir):
        for log in ls_(abs_logs_dir):
            data.append({
                'name': log,
                'path': os.path.join(relative_logs_dir, log)
            })

    return data[index:]

def get_test_batch_crashes(app, testbatch_id):
    result = db.session.query(TestCrash)\
                        .filter(TestCrash.test_batch_id == testbatch_id)\
                        .all()

    for crash in result:
        crash.trace_list = crash.trace.split(os.linesep)

    return result

def get_test_batch_video_recording(app, testbatch_id, only_total = False):
    data = []

    relative_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "video_recording"
    )

    abs_dir = os.path.join(
        app.brome.get_config_value('project:test_batch_result_path'),
        relative_dir
    )

    if os.path.isdir(abs_dir):
        for browser_dir in os.listdir(abs_dir):
            video_recording_list = os.listdir(os.path.join(abs_dir, browser_dir))

            for video_recording in video_recording_list:
                data.append({
                    'title': '%s - %s'%(video_recording.split('.')[0].replace('_', ' '), browser_dir.replace('_', ' ')),
                    'path': os.path.join(relative_dir, browser_dir, video_recording)
                })

    if only_total:
        return len(data)

    return data
