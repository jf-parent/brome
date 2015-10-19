Brome CLI
=========

In order to use Brome you must first create a brome object. The project template come with a `bro` python script that do just that::

    #!/usr/bin/env python

    import sys
    import os

    from brome import Brome

    from model.selector import selector_dict
    from model.test_dict import test_dict

    if __name__ == '__main__':

        HERE = os.path.abspath(os.path.dirname(__file__))

        brome = Brome(
            config_path = os.path.join(HERE, "config", "brome.yml"),
            selector_dict = selector_dict,
            test_dict = test_dict,
            browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"),
            absolute_path = HERE
        )

        brome.execute(sys.argv)

You provide Brome with a few things:

* `config_path`: this is the path to the brome yaml config (see :ref:`configuration`).
* `selector_dict` **[optional]**: this is the dictionary holding your selector (see :ref:`selector_variable`).
* `test_dict` **[optional]**: this is the dictionary holding your test description (see :ref:`assertion`).
* `browser_config_path`: this is the path to the browser yaml config (see :ref:`browsers`).
* `absolute_path`: the path of your project.

Execute
-------

To get started::

    $ ./bro -h
    >$ ./bro admin | run | webserver | list | find

To get help for one specific command::

    $ ./bro admin -h
    >usage: bro [-h] [--generate-config] [--reset] [--create-database]
           [--delete-test-states] [--delete-test-results] [--reset-database]
           [--delete-database] [--update-test]

    >Brome admin

    >optional flags:
    >  -h, --help            show this help message and exit
    >  --generate-config     Generate the default brome config
    >  --reset               Reset the database + delete the test batch results +
    >                        update the test table + delete all the test state
    >  --create-database     Create the project database
    >  --delete-test-states  Delete all the test states
    >  --delete-test-results Delete all the test batch results
    >  --reset-database      Reset the project database
    >  --delete-database     Delete the project database
    >  --update-test         Update the test in the database

Run
---

The run command can run your test remotely or locally.

Local
~~~~~

To run a test locally use the `-l` flag::

    $ ./bro run -l 'browser-id' -s 'test-name'

So if you want to run the test named `/path/to/project/tests/test_login.py` on firefox then use this command::

    $ ./bro run -l 'firefox' -s 'login'

Remote
~~~~~~

If you want to run your test remotely then use the `-r` flag::
    
    $ ./bro run -r 'firefox_virtualbox' -s 'login'

Brome config
~~~~~~~~~~~~

You can overwrite a brome config for one particular run with the `--brome-config` flag. Let say you want to disable the sound on a test crash and on an assertion failure::

    $ ./bro run -l 'firefox' -s 'login' --brome-config "runner:play_sound_on_test_crash=False,runner:play_sound_on_assertion_failure=False"

Test config
~~~~~~~~~~~

You can pass a config value to a test scenario also using `--test-config`::

    $ ./bro run -l 'firefox' -s 'login' --test-config "register=True,username='test'"

    #/path/to/project/tests/test_login.py
    from model.basetest import BaseTest

    class Test(BaseTest):

        name = 'Login'

        def run(self, **kwargs):

            if self._test_config.get('register'):
                self.app.register(username = self._test_config.get('username'))

Test discovery
~~~~~~~~~~~~~~

You have 3 ways of telling brome which test scenario to run.

Search
######

The first one is with the `-s` flag. The `-s` stand for search. Brome will search for a test scenario under your `tests` folder that start with the prefix `test_` and end with `.py`. If you want to run the scenario named `test_login.py` then search for `login`. You can also use a python list index here. Let say you want to run the test scenario index `2` then use `-s [2]`. To find out your test scenario index use the `list` command (see :ref:`list`). Python slice are also supported e.g.: `-s [3:7]` will run the test scenario index from 3 to 7.

Name
####

The second way is with the `-n` flag. The `-n` flag stand for name. If your test scenario doesn't start with the prefix `test_` then brome won't consider it when you use the search flag. The use case for this is when you have some code that you don't want to run automatically (e.g.: data creation, administrative stuff, etc)::

    $ ls /path/to/project/tests
    > register_user.py
    > test_login.py
    > test_register.py
    $ ./bro run -l 'firefox' -n 'register_user' #Work
    $ ./bro run -l 'firefox' -s 'register_user' #Won't work

This separation is pretty useful when you use the webserver to launch a test batch.

Test file
#########

The last way is by using a yaml file that contains a list of all the test scenario that you want to run (work only with the `-s` flag)::

    $ cat test_file.yml
    > - wait_until_present
    > - is_present
    > - assert_present

    $ ./bro run -l 'firefox' --test-file test_file.yml

Admin
-----

Reset
~~~~~

This command will reset the database, delete all the test files, update the test table and delete all the test states::

    $ ./bro admin --reset

Generate config
~~~~~~~~~~~~~~~

This command will generate a brome default config::

    $ ./bro admin --generate-config

It will overwrite your actual brome.yml config with the default value for each config.

Create database
~~~~~~~~~~~~~~~

This command is not useful unless you use a server database like MySQL. It is not necessary to use this command with SQLite::

    $ ./bro admin --create-database

Reset database
~~~~~~~~~~~~~~

This will delete the database and then recreate it::

    $ ./bro admin --reset-database

Delete database
~~~~~~~~~~~~~~~

This will delete the database::

    $ ./bro admin --delete-database

Delete test states
~~~~~~~~~~~~~~~~~~

This will delete all the pickle file found in `/path/to/project/tests/states/` (see :ref:`state`)::

    $ ./bro admin --delete-test-states

Delete test results
~~~~~~~~~~~~~~~~~~~

This will delete all the test batch data files found under your brome config `project:test_batch_result_path`::

    $ ./bro admin --delete-test-results

Update test
~~~~~~~~~~~

This command is not that useful since the test table is updated automatically but if you find that the test table has not been updated automatically the use this command to force it::

    $ ./bro admin --update-test

Webserver
---------

To start the webserver use the `webserver` command::

    $ ./bro webserver

This use the build in Flask webserver.

Tornado
~~~~~~~

If you want to start a tornado webserver instead use the `-t` flag::

    $ ./bro webserver -t

If you are over ssh and you want to start the webserver in the background and detach it from the current ssh session then use this bash command::

    $ nohup ./bro webserver -t &


.. _list:

List
----

To find out the index of your test scenario use the `list` command::

    $ ./bro list
    > [0]   login
    > [1]   register
    > [2]   logout

Find
----

The `find` command is use to find either a `test_id` or a `selector_variable`::

    $ ./bro find --test-id '#1'

    $ ./bro find --selector 'sv:login_username'
