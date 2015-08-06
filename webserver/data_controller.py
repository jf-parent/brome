#! -*- coding: utf-8 -*-

import os
from glob import glob

from brome.core.model.test_batch import TestBatch
from brome.webserver.extensions import db

def get_test_batch_list():
    data = db.session.query(TestBatch).all()

    return data

def get_test_batch_test_instance_log(app, testbatch_id, index):
    data = []

    relative_logs_dir = os.path.join(
        "tb_%s"%testbatch_id,
        "logs"
    )

    abs_logs_dir = os.path.join(
        app.config['TEST_BATCH_RESULT_PATH'],
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
        app.config['TEST_BATCH_RESULT_PATH'],
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
