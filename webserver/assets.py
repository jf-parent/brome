# -*- coding: utf-8 -*-

from flask_assets import Bundle, Environment

css = Bundle(
    "libs/jQueryui/jquery-ui.css",
    "libs/primeui/theme/bootstrap/theme.css",
    "libs/primeui/primeui-2.0-min.css",
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/all.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/jQueryui/jquery-ui.js",
    "libs/primeui/primeui-2.0-min.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/plugins.js",
    filters='jsmin',
    output="public/js/all.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
