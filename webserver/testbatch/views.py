# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("testbatch", __name__, url_prefix='/tb',
                      static_folder="../static")

@blueprint.route("/detail/<int:testbatch_id>")
@login_required
def detail(testbatch_id):
    data = {}
    data['is_running'] = True

    data['logs'] = []
    data['logs'].append({'name': 'Test register'})
    data['logs'].append({'name': 'Test login'})
    data['logs'].append({'name': 'Test logout'})
    data['logs'].append({'name': 'Test create block'})

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

    return render_template("testbatch/testresult.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/crash/<int:testbatch_id>")
@login_required
def crash(testbatch_id):
    data = {}
    data['crash_list'] = []
    data['crash_list'].append({'name': 'Test Login', 'trace': 'missing config'})
    data['crash_list'].append({'name': 'Test Registration', 'trace': 'missing config'})
    data['crash_list'].append({'name': 'Test Logout', 'trace': 'missing config'})
    data['crash_list'].append({'name': 'Test Create block', 'trace': 'missing config'})
    data['crash_list'].append({'name': 'Test Delete block', 'trace': 'missing config'})

    return render_template("testbatch/crash.html", testbatch_id = testbatch_id, data = data)

@blueprint.route("/list")
@login_required
def list():
    data = {}
    data['testbatchlist'] = []
    data['testbatchlist'].append({'id': 1, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: is running...'})
    data['testbatchlist'].append({'id': 2, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 3, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 4, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 5, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 6, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 7, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 8, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 9, 'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 10,'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})
    data['testbatchlist'].append({'id': 11,'timestamp_start': 'Started: 2015-07-29 17:00', 'timestamp_end': 'Ended: 2015-07-29 18:00'})

    return render_template("testbatch/list.html", data = data)
