# -*- coding: utf-8 -*-

"""Helper utilities and decorators."""

from subprocess import call
import os
import md5
import mimetypes
import re

from IPython import embed
from flask import flash, request, send_file, Response, current_app

def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)

def annotate_video(blueprint, title, obj_data):
    try:
        m = md5.new()
        m.update(title)
        video_hash = m.hexdigest()

        data = {}
        relative_video_folder = os.sep.join(obj_data['video_path'].split(os.sep)[:-1])
        video_folder = os.path.join(
            blueprint.app.brome.get_config_value('project:test_batch_result_path'),
            os.sep.join(obj_data['video_path'].split(os.sep)[:-1])
        )

        if obj_data['video_path'] == '0':
            return 'No video!', None

        data['title'] = "Bug (@%ss) %s"%(obj_data['video_time_position'], title)
        data['in'] = os.path.join(blueprint.app.brome.get_config_value('project:test_batch_result_path'), obj_data['video_path'])
        data['font_path'] = blueprint.app.brome.get_config_value("webserver:report")['font_path']
        data['copied_video_path'] = os.path.join(video_folder, 'copy-%s.mp4'%video_hash)
        data['annotated_video_path'] = os.path.join(video_folder, '%s.mp4'%video_hash)
        data['relative_annotated_video_path'] = os.path.join(relative_video_folder, '%s.mp4'%video_hash)

        script = """
            rm {annotated_video_path}
            cp {in} {copied_video_path}
            ffmpeg -i {copied_video_path} -vf "drawtext=':fontfile={font_path}: text='{title}': box=1: boxcolor=white@0.5: fontsize=32: y=(h - 30):" -acodec copy {annotated_video_path}
            rm {copied_video_path}
        """.format(**data)

        if obj_data['extra_data'].get('bounding_client_rect'):
            bounding_client_rect = obj_data['extra_data'].get('bounding_client_rect')
            data['box_start_time'] = int(obj_data['video_time_position'] - 5)
            data['box_end_time'] = int(obj_data['video_time_position'] + 1)
            data['box_x_position'] = int(bounding_client_rect['right']) + obj_data['extra_data']['video_x_offset']
            data['box_y_position'] = int(bounding_client_rect['bottom']) + obj_data['extra_data']['video_y_offset']
            data['box_h'] = int(bounding_client_rect['height'])
            data['box_w'] = int(bounding_client_rect['width'])

            script = """
                rm {annotated_video_path}
                cp {in} {copied_video_path}
                ffmpeg -i {copied_video_path} -vf "drawtext=':fontfile={font_path}: text='{title}': box=1: boxcolor=white@0.5: fontsize=32: y=(h - 30):, drawbox=enable='between(t,{box_start_time},{box_end_time})': x={box_x_position}: y={box_y_position}: c=red: h={box_h}: w={box_w}:" -acodec copy {annotated_video_path}
                rm {copied_video_path}
            """.format(**data)

        print script

        call(script, shell = True)

        return 'Success!', data['relative_annotated_video_path']
    except Exception as e:
        return unicode(e), None

def send_file_partial(path):
    #http://blog.asgaard.co.uk/2012/08/03/http-206-partial-content-for-flask-python
    range_header = request.headers.get('Range', None)
    if not range_header: return send_file(path)
    
    size = os.path.getsize(path)    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()
    
    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 
        206,
        mimetype=mimetypes.guess_type(path)[0], 
        direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv
