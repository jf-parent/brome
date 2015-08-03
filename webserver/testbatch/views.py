# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask.ext.login import login_required

blueprint = Blueprint("testbatch", __name__, url_prefix='/tb',
                      static_folder="../static")


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
