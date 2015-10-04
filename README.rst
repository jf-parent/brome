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

* Documentation: https://brome.readthedocs.org.

Features
--------

* Simple API
* Highly configurable
* Runner for Amazon EC2, Saucelabs, Virtualbox, Appium
* Javascript implementation of select, drag and drop, scroll into view
* IPython embed on assertion for debugging
* Video recording of the session
* Persistent test report
* Webserver
* Pdb integration
* Visual validation (Beta)
* Test state persistence system
* Browsermob proxy integration
* Support mobile easier (e.g.: click use Touch)

Quick-start
-----------

    ::

    $ cookiecutter https://github.com/brome-hq/cookiecutter-brome
    $ chmod +x bro
    $ pip install brome
    $ vim config/brome.yml
    $ ./bro admin --create-database
