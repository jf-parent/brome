#! -*- coding: utf-8 -*-

import os.path
import pickle

from brome.core.model.utils import *
from brome.core.model.stateful import Stateful
from brome.core.model.meta.base import Session
from brome.core.model.configurator import test_config_to_dict
from brome.core.model.test_instance import TestInstance

class BaseTest(object):

    def __init__(self, **kwargs):
        self._browser_instance = kwargs.get('browser_instance')
        self.pdriver = self._browser_instance.pdriver
        self._test_batch = kwargs.get('test_batch')
        self._name = kwargs.get('name')
        self._index = kwargs.get('index')
        self._test_instance = TestInstance(
            starting_timestamp = datetime.now(),
            name = self.name,
            testbatch = self._test_batch
        )

        self._session = Session()

        self._session.add(self._test_instance)
        self._session.commit()

        self.pdriver.test_instance = self._test_instance
        self.pdriver.session = self._session

        #TEST KWARGS
        self._test_config = test_config_to_dict(self._browser_instance.get_config_value("runner:test_config"))

        #LOGGING
        self.configure_logger()

    def save_state(self):
        self.info_log("Saving state")

        state = {}
        state = {key:value for (key, value) in self.__dict__.iteritems() if key[0] != '_'}
        del state['pdriver']

        effective_state = Stateful.cleanup_state(state)

        #Extract the server name
        server = urlparse(self.pdriver.current_url).netloc

        #State pickle name
        state_dir = os.path.join(
            self.pdriver.browser_instance.get_config_value("project:absolute_path"),
            "tests/states/"
        )
        create_dir_if_doesnt_exist(state_dir)

        state_pickle = os.path.join(
            state_dir,
            string_to_filename('%s_%s_%s.pkl'%(self._name.replace(' ', '_'), server, self._index))
        )

        with open(state_pickle,'wb') as s:
            pickle.dump(effective_state, s)

    def load_state(self):
        self.info_log("Loading state...")

        def set_pdriver(value):
            if Stateful in value.__class__.__bases__:
                value.pdriver = self.pdriver
            elif type(value) is list:
                for v in value:
                    set_pdriver(v)
            elif type(value) is dict:
                for k, v in value.iteritems():
                    set_pdriver(v)

        #Extract the server name
        server = urlparse(self.pdriver.current_url).netloc

        state_dir = os.path.join(
            self.pdriver.browser_instance.get_config_value("project:absolute_path"),
            "tests/states/"
        )

        state_pickle = os.path.join(
            state_dir,
            string_to_filename('%s_%s_%s.pkl'%(self._name.replace(' ', '_'), server, self._index))
        )

        if os.path.isfile(state_pickle):
            with open(state_pickle, 'rb') as s:
                state = pickle.load(s)
        else:
            self.info_log("No state found.")

            return False

        for key, value in state.iteritems():
            set_pdriver(value)

        self.__dict__.update(state)

        self.info_log("State loaded.")

        return True

    def configure_logger(self):
        pass

    def debug_log(self, msg):
        print '[debug_log] %s'%msg

    def info_log(self, msg):
        print '[info_log] %s'%msg

    def warning_log(self, msg):
        print '[warning_log] %s'%msg

    def error_log(self, msg):
        print '[error_log] %s'%msg

    def take_screenshot(self, name):
        pass

    def execute(self):
        try:
            self.before_run()

            self.run(**self._test_config)

            self.after_run()

        except Exception, e:
            self.error_log('Test failed')

            tb = traceback.format_exc()

            self.error_log('Crash: %s'%tb)

            self.fail()

            raise
        finally:
            self.end()

    def end(self):
        if self._browser_instance.get_config_value("runner:play_sound_on_test_finished"):
            say(self._browser_instance.get_config_value("runner:sound_on_test_finished"))

        self._test_instance.ending_timestamp = datetime.now()
        self._session.commit()

    def before_run(self):
        pass

    def after_run(self):
        pass

    def fail(self):
        if self._browser_instance.get_config_value("runner:play_sound_on_test_crash"):
            say(self._browser_instance.get_config_value("runner:sound_on_test_crash"))

        if self._browser_instance.get_config_value("runner:embed_on_test_crash"):
            self._browser_instance.pdriver.embed()
