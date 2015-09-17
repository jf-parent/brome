#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

##################################################
# ROUTE
##################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('%s.html'%path, title = path)

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 7777)
