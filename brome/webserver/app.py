# -*- coding: utf-8 -*-

import os
import logging

from flask import Flask, render_template
import flask_sijax

from brome.core.model import *
from brome.core.model.meta.base import Base
from brome.webserver.assets import assets
from brome.webserver.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    debug_toolbar,
)
from brome.webserver import public, admin, testbatch
from brome.core.model.utils import create_dir_if_doesnt_exist

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def create_app(brome):
    app = Flask(__name__)
    app.brome = brome

    app.config.update(brome.get_config_value("webserver:*"))

    app.config['SQLALCHEMY_DATABASE_URI'] = brome.get_config_value('database:sqlalchemy.url')
    app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/libs/sijax/')
    app.config["SIJAX_JSON_URI"] = '/static/libs/sijax/json2.js'

    app.temp_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'tmp'
    )

    create_dir_if_doesnt_exist(app.temp_path)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    @app.before_first_request
    def setup():
        Base.metadata.create_all(bind=db.engine)

    return app

def configure_logging(app):
    logger_name = 'brome_webserver'

    app.logger = logging.getLogger(logger_name)

    #Stream logger 
    if app.brome.get_config_value('webserver:streamlogger'):
        sh = logging.StreamHandler()
        app.logger.addHandler(sh)

    #File logger
    if app.brome.get_config_value('webserver:filelogger'):
        fh = logging.FileHandler(os.path.join(app.runner_dir, '%s.log'%logger_name))
        app.logger.addHandler(fh)

    brome.logger.setLevel(getattr(logging, self.get_config_value('webserver:logger_level')))

def register_extensions(app):
    assets.init_app(app)

    bcrypt.init_app(app)

    cache.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)

    debug_toolbar.init_app(app)

    flask_sijax.Sijax(app)

def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    public.views.blueprint.app = app

    app.register_blueprint(admin.views.blueprint)
    admin.views.blueprint.app = app

    app.register_blueprint(testbatch.views.blueprint)
    testbatch.views.blueprint.app = app

def register_errorhandlers(app):

    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)

        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
