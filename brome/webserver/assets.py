# -*- coding: utf-8 -*-

from flask_assets import Bundle, Environment

css = Bundle(
    "libs/jQueryui/jquery-ui.css",
    "libs/primeui/theme/bootstrap/theme.css",
    "libs/primeui/primeui-2.0-min.css",
    "libs/primeui/css/datagrid/datagrid.css", #http://forum.primefaces.org/viewtopic.php?f=16&t=42486
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/style.css",
    "libs/bootstrap_dialog/bootstrap-dialog.min.css",
    "libs/videojs/video-js.min.css",
    filters="cssmin",
    output="public/css/all.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/jQueryui/jquery-ui.js",
    "libs/primeui/primeui-2.0-hacked.js", #hacked version of primeui
    "libs/primeui/js/datagrid/datagrid.js", #http://forum.primefaces.org/viewtopic.php?f=16&t=42486
    "libs/bootstrap/dist/js/bootstrap.js",
    "libs/videojs/video.min.js",
    "js/plugins.js",
    "libs/bootstrap_dialog/bootstrap-dialog.min.js",
    filters='jsmin',
    output="public/js/all.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
