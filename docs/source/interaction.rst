Interactions
============

Proxy driver
------------

Get
###

Same as the selenium `get` method except that if the config `proxy_driver:intercept_javascript_error` is set to True then each time you call `get` it will inject the javascript code to intercept javascript error::

    pdriver.get("http://www.example.com")

Inject javascript script
########################

This method will inject the provided javascript script into the current page::

    pdriver.inject_js_script("https://code.jquery.com/jquery-2.1.4.min.js")
    
    js_path = os.path.join(
        pdriver.get_config_value("project:absolute_path"),
        "resources",
        "special_module.js"
    )
    pdriver.inject_js_script(js_path)

Init javascript error interception
##################################

This will inject the javascript code responsible of intercepting the javascript error::

    self._driver.execute_script("""
        window.jsErrors = [];
        window.onerror = function (errorMessage, url, lineNumber) {
            var message = 'Error: ' + errorMessage;
            window.jsErrors.push(message);
            return false;
        };
    """)

Print javascript error
######################

This will print the gathered javascript error using the logger::

    pdriver.print_javascript_error()

**Note** that each time you access the javascript error, the list holding them is reset.

Get javascript error
####################

This will return a string or a list of all the gathered javascript error::

    pdriver.get_javascript_error(return_type = 'string')

    pdriver.get_javascript_error(return_type = 'list')

**Note** that each time you access the javascript error, the list holding them is reset.

Pdb
###

This will start a python debugger::

    pdriver.pdb()

Note that calling `pdb` won't work in a multithread context, so whenever you use the -r switch with the `bro` executable the `pdb` call won't work.

Embed
#####

This will start a ipython embed::

    pdriver.embed()

    pdriver.embed(title = 'Ipython embed')

Note that calling `embed` won't work in a multithread context, so whenever you use the -r switch with the `bro` executable the `embed` call won't work.

Drag and drop
#############

The drag and drop have two implementation: one use javascript; the other use the selenium ActionChains::

    pdriver.drag_and_drop("sv:source", "sv:destination", use_javascript_dnd = True)

    pdriver.drag_and_drop("sv:source", "sv:destination", use_javascript_dnd = False)

    pdriver.drag_and_drop("sv:source", "sv:destination") #use_javascript_dnd will be initialize from the config `proxy_driver:use_javascript_dnd`

Take screenshot
###############

Take a screenshot::

    pdriver.get_config_value('runner:cache_screenshot')
    >>>True
    pdriver.take_screenshot('login screen')
    pdriver.take_screenshot('login screen') #won't save any thing to disc

    pdriver.get_config_value('runner:cache_screenshot')
    >>>False
    pdriver.take_screenshot('login screen')
    pdriver.take_screenshot('login screen') #first screenshot will be overridden

**Note:** If the `runner:cache_screenshot` config is set to True then screenshot sharing all the same name will be saved only once

Proxy element
-------------

Click
#####

Send keys
#########

Clear
#####

Highlight
#########

Scroll into view
################

Select all
##########
