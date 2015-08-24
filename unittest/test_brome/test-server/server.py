#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import json
import base64
import os.path
import os
from time import sleep
import logging
from IPython import embed

try:
    from flask import Flask, redirect, render_template, request, flash, jsonify
    from werkzeug.contrib.fixers import ProxyFix
except ImportError:
    print '*** flask is not installed'
    print 'pip install Flask'
    exit(1)

app = Flask(__name__)

##################################################
# ROUTE
##################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/intercept-javascript-error-test')
def intercept_javascript_error_test():
    return render_template('intercept-javascript-error-test.html')

@app.route('/select-all-test')
def select_all_test():
    return render_template('select-all-test.html')

@app.route('/selector-test')
def selector_test():
    return render_template('selector-test.html')

@app.route('/click-test')
def click_test():
    return render_template('click-test.html')

@app.route('/highlight-test')
def highlight_test():
    return render_template('highlight-test.html')

@app.route('/wait-until-visible-test')
def wait_until_visible_test():
    return render_template('wait_until_visible-test.html')

@app.route('/wait-until-not_visible-test')
def wait_until_not_visible_test():
    return render_template('wait_until_not_visible-test.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 7777)
