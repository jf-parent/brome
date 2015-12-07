Installation
============

Create the brome project using cookie-cutter
--------------------------------------------

Install cookie-cutter::

    $ [sudo] pip install cookiecutter

Create the brome project::

    $ mkdir brome_project
    $ cd brome_project
    $ cookiecutter https://github.com/brome-hq/cookiecutter-brome -f

Create a virtual env *[optional]*
---------------------------------

Install virtualenv and virtualenvwrapper::

    $ pip install virtualenv virtualenvwrapper

Add this line to your .bash_profile::

    source /usr/local/bin/virtualenvwrapper.sh

Reload your .bash_profile::

    $ source ~/.bash_profile

Create your virtualenv::

    $ mkvirtualenv venv

Activate the virtualenv::

    $ workon venv

Install brome
--------------

::

    $ pip install brome

