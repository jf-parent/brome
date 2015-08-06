# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, send_from_directory
from flask.ext.login import login_required

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
    data['screenshot_list'] = []
    data['screenshot_list'].append({'title': 'Empty bottle', 'path': 'image/sc1.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'User with long name', 'path': 'image/sc2.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Unavailable feed', 'path': 'image/sc3.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Super admin', 'path': 'image/sc4.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Temporary', 'path': 'image/sc5.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Special feed', 'path': 'image/sc6.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Sick of it', 'path': 'image/sc7.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Deleted block', 'path': 'image/sc8.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'User not logged', 'path': 'image/sc9.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Feed', 'path': 'image/sc10.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Application ready', 'path': 'image/sc11.png', 'browser_id': 'Chrome'})
    data['screenshot_list'].append({'title': 'Block', 'path': 'image/sc12.png', 'browser_id': 'Chrome'})

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
    data['result_list'] = []
    data['result_list'].append({'testid': 1, 'result': False, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 2, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 3, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 4, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 5, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 6, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 7, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 8, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 9, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 10, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 11, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 12, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 13, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 14, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 15, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 16, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 17, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 18, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 19, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 20, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 21, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 22, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})
    data['result_list'].append({'testid': 23, 'result': True, 'testname': 'This is the test name of the test', 'browserid': 'Chrome head', 'screenshot_path': 'image/crash.png'})

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
