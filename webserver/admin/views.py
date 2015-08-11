# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask.ext.login import login_required
from IPython import embed

from brome.webserver.admin.forms import ConfigForm

blueprint = Blueprint("admin", __name__, url_prefix='/admin',
                      static_folder="../static")

@blueprint.route("/")
@login_required
def members():
    return render_template("admin/members.html")

@blueprint.route("/configuration/", methods=['GET', 'POST'])
@login_required
def configuration():
    form = ConfigForm(blueprint.app)

    if request and request.method in ("PUT", "POST"):
        flash("The brome configuration has been updated successfully!", 'success')
        form.save(request.form)
        return redirect(url_for('public.home'))

    return render_template("admin/configuration.html", form = form)
