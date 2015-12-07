===============================
brome
===============================

.. image:: https://img.shields.io/travis/brome-hq/brome.svg
        :target: https://travis-ci.org/brome-hq/brome

.. image:: https://img.shields.io/pypi/v/brome.svg
        :target: https://pypi.python.org/pypi/brome

.. image:: https://readthedocs.org/projects/brome/badge/?version=latest
    :target: http://brome.readthedocs.org/en/release
    :alt: Documentation Status

Framework for Selenium

* Documentation: https://brome.readthedocs.org
* Blog: http://brome-hq.logdown.com/

Features
--------

* Simple API
* Focused on test stability and uniformity
* Highly configurable
* Runner for Amazon EC2, Saucelabs, Browserstack, Virtualbox and Appium
* Javascript implementation of select, drag and drop, scroll into view
* IPython embed on assertion for debugging
* Session Video recording
* Network capture with mitmproxy (firefox & chrome)
* Persistent test report
* Webserver
* Test state persistence system
* Support mobile easier (e.g.: click use Touch)

Quick-start
-----------

    ::

    $ cookiecutter https://github.com/brome-hq/cookiecutter-brome -f
    $ chmod +x bro
    $ pip install brome
    $ vim config/brome.yml
