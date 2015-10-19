#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, json

app = Flask(__name__)

##################################################
# ROUTE
##################################################

@app.route('/request/<int:value>')
def request(value):
    if value < 10:
        data = json.dumps({'success': False, 'value': value})
        return data
    else:
        data = json.dumps({'success': True, 'value': value})
        return data

if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 7777)
