# -*- coding: utf-8 -*-

from time import sleep
import subprocess

from flask import Blueprint, render_template, flash, redirect, url_for, request, send_from_directory, g
import flask_sijax
from flask.ext.login import login_required
from IPython import embed

from brome.webserver.testbatch.forms import LaunchForm
from brome.core.model.utils import *
from brome.webserver import data_controller

blueprint = Blueprint("testbatch", __name__, url_prefix='/tb',
                      static_folder="../static")

websocket_process = None

def delete_test_batch(obj_response, testbatch_id):
    data_controller.delete_test_batch(blueprint.app, testbatch_id)
    flash("The test batch (%s) have been deleted!"%testbatch_id, 'success')
    obj_response.script("window.location = '%s';"%url_for("testbatch.list"))

def stop_test_batch(obj_response, testbatch_id):
    data_controller.stop_test_batch(blueprint.app, testbatch_id)
    flash("The test batch (%s) will be stop as soon as possible..."%testbatch_id, 'success')
    obj_response.script("window.location = '%s';"%url_for("testbatch.list"))

@blueprint.route("/vnc/<string:host>")
@login_required
def vnc(host):
    #TODO make this configurable
    return render_template("testbatch/vnc.html", title = 'VNC', host = host, port = 5900, password = '1asdf!!')

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
        else:
            if test_batch.ending_timestamp:
                obj_response.script("clearInterval(%s);"%interval_id)

        if test_batch.ending_timestamp:
            total_execution_time = data_controller.get_total_execution_time(blueprint.app, testbatch_id)

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
            obj_response.script("$('#total_failed_tests').html(%s)"%test_batch.total_failed_tests)

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('delete_test_batch', delete_test_batch)
        g.sijax.register_callback('stop_test_batch', stop_test_batch)
        g.sijax.register_callback('update_info', update_info)
        return g.sijax.process_request()

    data = {}
    data['test_batch'] = data_controller.get_test_batch_detail(blueprint.app, testbatch_id)
    data['logs'] = data_controller.get_test_batch_test_instance_log(blueprint.app, testbatch_id, 0)
    data['runner_log'] = data_controller.get_test_batch_log(blueprint.app, testbatch_id)

    show_video_capture = blueprint.app.brome.get_config_value("webserver:SHOW_VIDEO_CAPTURE")
    show_test_instances = blueprint.app.brome.get_config_value("webserver:SHOW_TEST_INSTANCES")

    return render_template(
        "testbatch/detail.html",
        testbatch_id = testbatch_id,
        data = data,
        show_test_instances = show_test_instances,
        show_video_capture = show_video_capture
    )

@blueprint.route("/screenshot/<int:testbatch_id>")
@login_required
def screenshot(testbatch_id):
    data = {}
    data['screenshot_list'] = data_controller.get_test_batch_screenshot(blueprint.app, testbatch_id)

    return render_template("testbatch/screenshot.html", testbatch_id = testbatch_id, data = data)

@flask_sijax.route(blueprint, "/test_instances/<int:testbatch_id>")
@login_required
def test_instances(testbatch_id):
    global websocket_process
    data = {}
    data['test_instance_list'] = data_controller.get_active_test_instance(blueprint.app, testbatch_id)

    def start_websocket(obj_response, host):
        global websocket_process
        webserver_root = os.sep.join(os.path.abspath(os.path.dirname(__file__)).split(os.sep)[:-1])
        websockify_exe = os.path.join(
            webserver_root,
            "websockify"
        )
    
        src_addr = 'localhost'
        src_port = 6880
        dest_addr = host
        dest_port = 5900

        command = [
            "%s%s%s"%(websockify_exe, os.sep, "websockify.py"),
            '%s:%s'%(src_addr, src_port),
            '%s:%s'%(dest_addr, dest_port)
        ]
        if not websocket_process:
            process = subprocess.Popen(command)

        obj_response.script("""
            $('[name = "startWebsocket"]').each(function( index ) {
                  $(this).prop('disabled', true);
              });
        """)

        websocket_process = process

    def stop_websocket(obj_response):
        global websocket_process

        websocket_process.kill()

        obj_response.script("""
            $('[name = "startWebsocket"]').each(function( index ) {
                  $(this).prop('disabled', false);
              });
        """)

        websocket_process = None

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('start_websocket', start_websocket)
        g.sijax.register_callback('stop_websocket', stop_websocket)
        return g.sijax.process_request()

    websocket_alive = websocket_process is not None

    return render_template("testbatch/test_instances.html", testbatch_id = testbatch_id, data = data, websocket_alive = websocket_alive)

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
