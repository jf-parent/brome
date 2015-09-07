#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Selector'

    def run(self, **kwargs):

        self.info_log("Running...")

        #TEST
        self.app.go_to("selector_test")

        ###TAG NAME
        #FIND ALL BY TAG NAME
        elements = self.pdriver.find_all("tn:h1")
        assert len(elements) == 2

        #FIND BY TAG NAME
        element = self.pdriver.find("tn:h1")
        assert element.get_attribute('id') == '1'

        #FIND LAST BY TAG NAME
        element = self.pdriver.find_last("tn:h1")
        assert element.get_attribute('id') == '2'

        #FIND BY TAG NAME DOESNT EXIST
        element = self.pdriver.find("tn:thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY TAG NAME DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("tn:thisdoesntexist", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###NAME
        #FIND ALL BY NAME
        elements = self.pdriver.find_all("nm:name-selector")
        assert len(elements) == 2

        #FIND BY NAME
        element = self.pdriver.find("nm:name-selector")
        assert element.get_attribute('id') == '3'

        #FIND LAST BY NAME
        element = self.pdriver.find_last("nm:name-selector")
        assert element.get_attribute('id') == '4'

        #FIND BY NAME DOESNT EXIST
        element = self.pdriver.find("nm:thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY NAME DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("nm:thisdoesntexist", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###CLASS NAME
        #FIND ALL BY CLASS NAME
        elements = self.pdriver.find_all("cn:class-selector")
        assert len(elements) == 2

        #FIND BY CLASS NAME
        element = self.pdriver.find("cn:class-selector")
        assert element.get_attribute('id') == '2'

        #FIND LAST BY CLASS NAME
        element = self.pdriver.find_last("cn:class-selector")
        assert element.get_attribute('id') == '5'

        #FIND BY CLASS NAME DOESNT EXIST
        element = self.pdriver.find("cn:thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY CLASS NAME DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("cn:thisdoesntexist", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###ID
        #FIND ALL BY ID
        elements = self.pdriver.find_all("id:1")
        assert len(elements) == 1

        #FIND BY ID
        element = self.pdriver.find("id:1")
        assert element.get_attribute('id') == '1'

        #FIND LAST BY ID
        element = self.pdriver.find_last("id:1")
        assert element.get_attribute('id') == '1'

        #FIND BY ID DOESNT EXIST
        element = self.pdriver.find("id:thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY ID DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("id:thisdoesntexist", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###XPATH
        #FIND ALL BY XPATH
        elements = self.pdriver.find_all("xp://h1")
        assert len(elements) == 2

        #FIND BY XPATH
        element = self.pdriver.find("xp://*[@id = 1]")
        assert element.get_attribute('id') == '1'

        #FIND LAST BY XPATH
        element = self.pdriver.find_last("xp://h1")
        assert element.get_attribute('id') == '2'

        #FIND BY XPATH DOESNT EXIST
        element = self.pdriver.find("xp://*[@class = 'thisdoesntexist']", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY XPATH DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("xp://*[@class = 'thisdoesntexist']", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###CSS
        #FIND ALL BY CSS
        elements = self.pdriver.find_all("cs:h1")
        assert len(elements) == 2

        #FIND BY CSS
        element = self.pdriver.find("cs:h1")
        assert element.get_attribute('id') == '1'

        #FIND LAST BY CSS
        element = self.pdriver.find_last("cs:h1")
        assert element.get_attribute('id') == '2'

        #FIND BY CSS DOESNT EXIST
        element = self.pdriver.find("cs:.thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY CSS DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("cs:.thisdoesntexist", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###LINK TEXT
        #FIND ALL BY LINK TEXT
        elements = self.pdriver.find_all("lt:link-text-selector")
        assert len(elements) == 2

        #FIND BY LINK TEXT
        element = self.pdriver.find("lt:link-text-selector")
        assert element.get_attribute('id') == '6'

        #FIND LAST BY LINK TEXT
        element = self.pdriver.find_last("lt:link-text-selector")
        assert element.get_attribute('id') == '7'

        #FIND BY LINK TEXT DOESNT EXIST
        element = self.pdriver.find("lt:text-selector", raise_exception = False)
        assert element == None

        #FIND BY LINK TEXT DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("lt:thisdoesntexit", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True

        ###PARTIAL LINK TEXT
        #FIND ALL BY PARTIAL LINK TEXT
        elements = self.pdriver.find_all("pl:text-selector")
        assert len(elements) == 2

        #FIND BY PARTIAL LINK TEXT
        element = self.pdriver.find("pl:text-selector")
        assert element.get_attribute('id') == '6'

        #FIND LAST BY PARTIAL LINK TEXT
        element = self.pdriver.find_last("pl:text-selector")
        assert element.get_attribute('id') == '7'

        #FIND BY PARTIAL LINK TEXT DOESNT EXIST
        element = self.pdriver.find("pl:thisdoesntexist", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY PARTIAL LINK TEXT DOESNT EXIST RAISE EXCEPTION
        try:
            self.pdriver.find("pl:thisdoesntexit", wait_until_visible = False)
            assert False
        except NoSuchElementException:
            assert True
