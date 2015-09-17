#! -*- coding: utf-8 -*-

from .base_instance import BaseInstance

class LocalhostInstance(BaseInstance):

    def tear_down(self):
        print 'Tear down'
