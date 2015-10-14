State
=====

The brome's state system allow you to save a test state in order to speed up and ease your test flow.

You need to set the config `project:url` in order to use the state since the state name is created with the host name and the test name::

    self.pdriver.get_config_value("project:url")
    >>>'http://example.com'

    self._name
    >>>Test1

    self.get_state_pickle_path()
    >>>/path/to/project/tests/states/Test1_example.com.pkl

This is mainly to support switching the host name in your test. Maybe sometime the code to be tested is on another server, so the state won't exist on this server.

Stateful mixin
--------------

The brome's state system will save the following build-in python type:

* str
* unicode
* int
* float
* dict
* list

However not build-in python class won't be saved into the state unless they inherit the Stateful mixin. Here is an example::
    
    #/path/to/project/tests/test_1.py
    from brome.core.model.stateful import Stateful

    class User(Stateful):

        def __init__(self, pdriver, username):
            self.pdriver = pdriver
            self.username = username

    class UnStateful(object):
        pass

    class Test(BaseTest):

        name = 'State'

        def create_state(self):
            self.unstateful = UnStateful()
            self.stateful = User(self.pdriver, 'test')
            self.int_ = 1
            self.float_ = 0.1
            self.unicode_ = u'test'
            self.str_ = 'str'
            self.list_ = [1,2]
            self.dict_ = {'key' : 1}

        def run(self, **kwargs):

            self.info_log("Running...")

            #TEST
            assert not hasattr(self, 'unstateful')

            assert hasattr(self, 'stateful')

            assert hasattr(self, 'int_')

            assert hasattr(self, 'float_')

            assert hasattr(self, 'unicode_')

            assert hasattr(self, 'str_')

            assert hasattr(self, 'list_')

            assert hasattr(self, 'dict_')

**Note**: Your stateful class must accept the pdriver in his __init__ function::

    from brome.core.model.stateful import Stateful

    class User(Stateful):

        def __init__(self, pdriver, username):
            self.pdriver = pdriver #<-- this
            self.username = username

The state will only be cleaned when it is loaded; so unstateful object will be in the locals() of the test object on the first run but not on the subsequent run. The cleaning function of the state is recursive, so unstateful object found in dict and list will be clearned up also. The stateful cleanup is mainly to satisfy the pickle python module...

Create state
------------

You can either use the automatic state creation (recommended) or create it manually.

Automatic state creation
~~~~~~~~~~~~~~~~~~~~~~~~

::

    class Test(BaseTest):

        name = 'Test'

        def create_state(self):
            self.dict_ = {'key' : 1}

        def run(self, **kwargs):

            self.info_log("Running...")

            #TEST
            self.dict_['key']

Manual state creation
~~~~~~~~~~~~~~~~~~~~~~~~

::

    #/path/to/project/tests/test_1.py
    class Test(BaseTest):
        
        name = 'Test 1'

        #...

        def run(self, **kwargs):

            #...

            state_loaded = self.load_state()
            if not state_loaded:
                self.string_1 = 'test'

                self.save_state()

            self.info_log(self.string_1)

Loading state
-------------

If you use the automatic state management them the state will be loaded automatically if one exist. The test logger will tell you if a state was found or not.

If you created the state manually them you also need to load it manually::

    #/path/to/project/tests/test_1.py
    class Test(BaseTest):
        
        name = 'Test 1'

        #...

        def run(self, **kwargs):

            #...

            state_loaded = self.load_state()

            if state_loaded:
                #Now you have access to the object that were saved in the state
                self.info_log(self.string_1)

Deleting state
--------------

Deleting a particular state
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to delete a particular test's state you can tell the bro executable to delete it before running the test::

    $ ./bro run -l firefox -s "test_1" --test-config "delete_state=True"

or delete it manually::

    $ rm /path/to/project/tests/states/teststate.pkl

Deleting all the states
~~~~~~~~~~~~~~~~~~~~~~~

If you want to delete all the states, the bro executable have a command for that::

    $ ./bro admin --delete-test-states

Or delete them manually::

    $ rm /path/to/project/tests/states/*.pkl

