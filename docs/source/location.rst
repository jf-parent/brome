Locating Elements
=================

Find methods
------------

Use the `proxy_driver` (`pdriver`) to locate element on the web page. Three methods exist::
    
    pdriver.find("sv:selector_variable")

    pdriver.find_last("nm:form")

    pdriver.find_all("tn:div")

The find method accept three kwargs::

    pdriver.find("nm:button", raise_exception = False)

    pdriver.find_all("id:1", wait_until_visible = False)

    pdriver.find_last("cs:div > span", wait_until_present = False, raise_exception = True)

    pdriver.find_all(
        "sv:selector_variable",
        wait_until_visible = True,
        wait_until_present = False,
        raise_exception = True
    )

The defaults for the kwargs wait_until_present, wait_until_visible and raise_exception can be set respectively with:
* proxy_driver:wait_until_present_before_find
* proxy_driver:wait_until_visible_before_find
* proxy_driver:raise_exception

The `find` and `find_last` method return a `proxy_element`.

The `find_all` method return a `proxy_element_list`.

By id
#####

::

    pdriver.find("id:button-1")

By css selector
###############

::

    pdriver.find("cs:div > span")

By name
#######

::

    pdriver.find("nm:button-1")

By class name
#############

::

    pdriver.find("cn:button")

By tag name
###########

::

    pdriver.find_all("tn:div")

By link text
############

::

    pdriver.find("lt:register now!")

By partial link text
####################

::

    pdriver.find("pl:register")

By selector variable
####################

::

    pdriver.find("sv:button_1")

List of selectors
-----------------

If you want to create a selector from multiple selector you can pass a list of selector to the `find_*` method::

    pdriver.find(["sv:selector_v1", "sv:selector_v2", "xp://*[contains(@class, 'button')]"])

Selectors validation
--------------------

The xpath and css selector will be validated if the config `proxy_driver:validate_xpath_selector` and `proxy_driver:validate_css_selector` are set to true.

.. _selector_variable:

Selector variable dictionary
----------------------------

A selector dictionary can be provided to brome::

    selector_dict = {}
    selector_dict['example_find_by_tag_name'] = "tn:a"
    selector_dict['example_find_by_id'] = "id:1"
    selector_dict['example_find_by_xpath'] = "xp://*[@class = 'xpath']"
    selector_dict['example_find_by_partial_link_text'] = "pl:partial link text"
    selector_dict['example_find_by_link_text'] = "lt:link text"
    selector_dict['example_find_by_css_selector'] = "cs:.classname"
    selector_dict['example_find_by_classname'] = "cn:classname"
    selector_dict['example_find_by_name'] = "nm:name"
    selector_dict['example_multiple_selector'] = {
        "default" : "xp://*[contains(@class, 'default')]",
        "chrome|iphone|android" : "xp://*[contains(@class, 'special')]"
    }

    brome = Brome(
        config_path = os.path.join(HERE, "config", "brome.yml"),
        selector_dict = selector_dict, #<--- this dict
        test_dict = test_dict,
        browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"),
        absolute_path = HERE
    )

So later on in your code you can use the selector variable to find elements::

    pdriver.find("sv:example_find_by_name")

Also a selector variable can vary from browser to browser::

    selector_dict['example_multiple_selector'] = {
        "default" : "xp://*[contains(@class, 'default')]",
        "chrome|iphone|android" : "xp://*[contains(@class, 'special')]"
    }

It support the browserName, version and platform returned by the pdriver._driver.capabilities

Plain selenium methods
----------------------

If you want to use the selenium location methods just use::

    pdriver._driver.find_element_by_id
    pdriver._driver.find_element_by_name
    pdriver._driver.find_element_by_xpath
    pdriver._driver.find_element_by_link_text
    pdriver._driver.find_element_by_partial_link_text
    pdriver._driver.find_element_by_tag_name
    pdriver._driver.find_element_by_class_name
    pdriver._driver.find_element_by_css_selector
    pdriver._driver.find_elements_by_name
    pdriver._driver.find_elements_by_xpath
    pdriver._driver.find_elements_by_link_text
    pdriver._driver.find_elements_by_partial_link_text
    pdriver._driver.find_elements_by_tag_name
    pdriver._driver.find_elements_by_class_name
    pdriver._driver.find_elements_by_css_selector

Note that this will return a selenium webelement and not a `proxy_element` or `proxy_element_list`
