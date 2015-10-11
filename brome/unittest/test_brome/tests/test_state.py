#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest
from model.user import User

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
