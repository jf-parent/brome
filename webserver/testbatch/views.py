# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, send_from_directory
from flask.ext.login import login_required
from IPython import embed

from brome.webserver import data_controller

blueprint = Blueprint("testbatch", __name__, url_prefix='/tb',
                      static_folder="../static")

@blueprint.route("/file/<path:filename>")
@login_required
def test_batch_report_file(filename):
    return send_from_directory(blueprint.app.config['TEST_BATCH_RESULT_PATH'], filename)

@blueprint.route("/launch")
@login_required
def launch():
    data = {}
    data['browser_list'] = []
    data['browser_list'].append({'id': 'Firefox', 'icon': 'fa-firefox'})
    data['browser_list'].append({'id': 'Safari', 'icon': 'fa-safari'})
    data['browser_list'].append({'id': 'Chrome', 'icon': 'fa-chrome'})
    data['browser_list'].append({'id': 'Iphone', 'icon': 'fa-mobile'})
    data['browser_list'].append({'id': 'Ipad', 'icon': 'fa-tablet'})
    data['browser_list'].append({'id': 'Android', 'icon': 'fa-android'})
    data['browser_list'].append({'id': 'Internet Explorer', 'icon': 'fa-internet-explorer'})

    data['test_list'] = []
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})
    data['test_list'].append({'name': 'Test Register'})

    return render_template("testbatch/launch.html", data = data)

@blueprint.route("/detail/<int:testbatch_id>")
@login_required
def detail(testbatch_id):
    data = {}
    data['is_running'] = True

    data['logs'] = data_controller.get_test_batch_test_instance_log(blueprint.app, testbatch_id, 0)

    return render_template("testbatch/detail.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/screenshot/<int:testbatch_id>")
@login_required
def screenshot(testbatch_id):
    data = {}

    data['screenshot_list'] = data_controller.get_test_batch_screenshot(blueprint.app, testbatch_id)

    return render_template("testbatch/screenshot.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/videocapture/<int:testbatch_id>")
@login_required
def videocapture(testbatch_id):
    data = {}

    return render_template("testbatch/videocapture.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/testresult/<int:testbatch_id>")
@login_required
def testresult(testbatch_id):
    data = {}

    data['result_list'] = data_controller.get_test_batch_test_result(blueprint.app, testbatch_id)

    return render_template("testbatch/testresult.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/crash/<int:testbatch_id>")
@login_required
def crash(testbatch_id):
    data = {}
    data['crash_list'] = data_controller.get_test_batch_crashes(blueprint.app, testbatch_id)

    return render_template("testbatch/crash.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/list")
@login_required
def list():
    data = {}

    data['testbatch_list'] = data_controller.get_test_batch_list()

    return render_template("testbatch/list.html", data = data)
