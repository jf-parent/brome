# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask.ext.login import login_required

from brome.core.model.configurator import default_config, ini_to_dict

blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    return render_template("admin/members.html")

@blueprint.route("/configuration")
@login_required
def configuration():
    data = default_config
    config = ini_to_dict(blueprint.app.brome_config_path)
    
    for section_key, section_item in config.iteritems():

        #Skip the webserver config
        if section_key == 'webserver':
            continue

        for option_key, option_item in section_item.iteritems():

            #User defined section
            if not data.has_key(section_key):
                data[section_key] = {}
                data[section_key][option_key] = {
                    'value': option_item,
                    'type': 'input',
                    'title': option_key
                }

            else:
                #User defined option
                if not data[section_key].has_key(option_key):
                    data[section_key][option_key] = {
                        'value': option_item,
                        'type': 'input',
                        'title': option_key
                    }
                else:
                    data[section_key][option_key]['value'] = option_item

    return render_template("admin/configuration.html", data = data)
