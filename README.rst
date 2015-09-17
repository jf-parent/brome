===============================
brome
===============================

.. image:: https://img.shields.io/pypi/v/brome.svg
        :target: https://pypi.python.org/pypi/brome


Framework for Selenium

* Free software: ISC license
* Documentation: https://brome.readthedocs.org.

Features
--------

* Simple API
* Runner for Amazon EC2
* Saucelabs runner
* Highly configurable
* IPython embed on assertion for debugging
* Video recording of the session
* Persistent test report
* Webserver
* Pdb integration
* Support Appium
* Visual validation (Beta)

Quick-start
-----------

    ::

    $ cookiecutter https://github.com/worker-9/cookiecutter-brome
    $ chmod +x bro
    $ ./bro install
    $ vim config/brome.yml
    $ ./bro admin --create-database
