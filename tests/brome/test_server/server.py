#!/usr/bin/env python

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
    return render_template('%s.html' % path, title=path)


def create_app(host='localhost', port=1771, debug=True):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    create_app()
