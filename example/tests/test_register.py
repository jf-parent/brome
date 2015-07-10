#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest
from model.user import User
from model.bad_stuff import BadStuff

class Test(BaseTest):

    name = 'Register'

    def run(self, **kwargs):
        self.pdriver.get("http://reddit.local/")

        if not self.load_state():
            self.user = User(pdriver = self.pdriver, name = 'test')
            self.bad_stuff = BadStuff(pdriver = self.pdriver)
            self.integer = 1
            self.float_ = 1.0
            self.dict_ = {'test':[1,[1, [1,2,[self.bad_stuff],2,[self.bad_stuff], User(pdriver= self.pdriver, name = 'test1')]]], 'bad_stuff': self.bad_stuff, 'shit_hole': [self.bad_stuff, [self.bad_stuff, 1, 2]]}
            self.list_ = [self.bad_stuff, 'test1', [self.bad_stuff, {'b':self.bad_stuff, 'good':{'test': [self.bad_stuff,4],'bb':self.bad_stuff, 'dd':[1,1,self.bad_stuff]}}]]
            self.unicode_ = u'test'
            self.save_state()

        self.pdriver.embed()

        """
        self.pdriver.take_screenshot()
        self.pdriver.take_screenshot('test')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#3')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#2')
        self.pdriver.assert_visible("xp://*[@class = 'test')]", '#2')
        self.pdriver.assert_visible("xp://*[@class = 'test')]", '#1')
        self.pdriver.assert_not_visible("xp://*[@class = 'test')]", '#1')
        self.pdriver.find_all("xp://*[@class = 'test')]")
        """
