# -*- coding: utf-8 -*-

from time import sleep
import subprocess

from flask import Blueprint, render_template, flash, redirect, url_for, request, send_from_directory, g
import flask_sijax
from flask.ext.login import login_required

from brome.webserver.testbatch.forms import LaunchForm
from brome.core.model.utils import *
from brome.webserver import data_controller

blueprint = Blueprint("testbatch", __name__, url_prefix='/tb',
                      static_folder="../static")

def delete_test_batch(obj_response, testbatch_id):
    data_controller.delete_test_batch(blueprint.app, testbatch_id)
    obj_response.alert('The test batch (%s) has been deleted'%testbatch_id)

def stop_test_batch(obj_response, testbatch_id):
    data_controller.stop_test_batch(blueprint.app, testbatch_id)
    obj_response.alert('The test batch (%s) will be stop as soon as possible...'%testbatch_id)

@blueprint.route("/vnc/<string:host>")
@login_required
def vnc(host):
    websockify_exe = blueprint.app.brome.get_config_value('webserver:WEBSOCKIFY_EXE')
    
    src_addr = 'localhost'
    src_port = 6880
    dest_addr = host
    dest_port = 5900

    kill_by_found_string_in_cmdline('Python', 'websockify')

    command = [
        websockify_exe,
        '%s:%s'%(src_addr, src_port),
        '%s:%s'%(dest_addr, dest_port)
    ]
    #print command
    subprocess.Popen(command)

    return render_template("testbatch/vnc.html", title = 'Test')

@blueprint.route("/file/<path:filename>")
@login_required
def test_batch_report_file(filename):
    return send_from_directory(blueprint.app.brome.get_config_value('project:test_batch_result_path'), filename)

@blueprint.route("/launch/", methods=['GET', 'POST'])
@login_required
def launch():
    form = LaunchForm(blueprint.app)

    if request and request.method in ("PUT", "POST"):
        success, msg = form.start_test_batch(request.form)
        if success:
            flash("The test batch has been started!", 'success')
            sleep(2)
            return redirect(url_for('testbatch.list'))
        else:
            flash(msg, 'warning')

    return render_template("testbatch/launch.html", form = form)

@flask_sijax.route(blueprint, "/detail/<int:testbatch_id>")
@login_required
def detail(testbatch_id):
    def update_info(obj_response, testbatch_id, interval_id, runner_log_length, current_progress):
        test_batch = data_controller.get_test_batch_detail(blueprint.app, testbatch_id)
        test_batch_log = data_controller.get_test_batch_log(blueprint.app, testbatch_id)

        if runner_log_length < len(test_batch_log):
            obj_response.script("""
                    var logs = "%s".split("|");

                    logs.forEach(function(log) {
                        $('#runnerlog').append('<h6>' + log + '</h6>');
                    });
            """%("|".join(test_batch_log[runner_log_length:])))

        if test_batch.ending_timestamp:
            total_execution_time = data_controller.get_total_execution_time(blueprint.app, testbatch_id)

            obj_response.script("clearInterval(%s);"%interval_id)
            obj_response.script("$('#testprogressdiv').remove();")
            obj_response.script("$('#testexecutiontimespan > strong').html('%s');"%total_execution_time)
            obj_response.script("$('#testexecutiontimediv').show();")
        else:
            progress = int(float(test_batch.total_finished_tests) / float(test_batch.total_tests) * 100)
            if str(progress) != current_progress.replace('%', ''):
                obj_response.script("$('#testprogress').puiprogressbar('option', 'value', %s);"%progress)

            obj_response.script("$('#total_crashes').html(%s)"%test_batch.total_crashes)
            obj_response.script("$('#total_executing_tests').html(%s)"%test_batch.total_executing_tests)
            obj_response.script("$('#total_finished_tests').html(%s)"%test_batch.total_finished_tests)
            obj_response.script("$('#total_screenshots').html(%s)"%test_batch.total_screenshots)
            obj_response.script("$('#total_test_results').html(%s)"%test_batch.total_test_results)

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('delete_test_batch', delete_test_batch)
        g.sijax.register_callback('stop_test_batch', stop_test_batch)
        g.sijax.register_callback('update_info', update_info)
        return g.sijax.process_request()

    data = {}
    data['test_batch'] = data_controller.get_test_batch_detail(blueprint.app, testbatch_id)
    data['logs'] = data_controller.get_test_batch_test_instance_log(blueprint.app, testbatch_id, 0)
    data['runner_log'] = data_controller.get_test_batch_log(blueprint.app, testbatch_id)

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

@flask_sijax.route(blueprint, "/list")
@login_required
def list():
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('delete_test_batch', delete_test_batch)
        g.sijax.register_callback('stop_test_batch', stop_test_batch)
        return g.sijax.process_request()

    data = {}
    data['testbatch_list'] = data_controller.get_test_batch_list()

    return render_template("testbatch/list.html", data = data)
