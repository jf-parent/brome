# -*- coding: utf-8 -*-

from flask import Flask, render_template

from brome.core.model import *
from brome.core.model.meta.base import Base
from brome.webserver.webserver.assets import assets
from brome.webserver.webserver.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    debug_toolbar,
)
from brome.webserver.webserver import public, user

def create_app(config_object):
    app = Flask(__name__)
    app.config.update(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    @app.before_first_request
    def setup():
        Base.metadata.create_all(bind=db.engine)

    return app

def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    return None

def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
