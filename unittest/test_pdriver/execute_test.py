#!/usr/bin/env python

import unittest
from selenium import webdriver

from brome.core.models.utils import *
from brome.core.models.proxy_driver import ProxyDriver

class Test(unittest.TestCase):
    def setUp(self):
        self.pdriver = ProxyDriver(webdriver.Firefox())

    def tearDown(self):
        self.pdriver.close()

    def test_selector(self):
        self.pdriver.get("localhost:7777/selector-test")

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("tn:thisdoesntexist", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("nm:thisdoesntexist", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("cn:thisdoesntexist", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("id:thisdoesntexist", wait_until_visible = False))

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
        element = self.pdriver.find("xp://*[@class = 'thisdoesntexist')]", raise_exception = False, wait_until_visible = False)
        assert element == None

        #FIND BY XPATH DOESNT EXIST RAISE EXCEPTION
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("xp://*[@class = 'thisdoesntexist')]", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("cs:.thisdoesntexist", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("lt:thisdoesntexit", wait_until_visible = False))

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
        self.assertRaises(NoSuchElementException, lambda: self.pdriver.find("pl:thisdoesntexit", wait_until_visible = False))

    def test_highlight(self):
        self.pdriver.get("localhost:7777/highlight-test")

        element = self.pdriver.find("id:1")

        element.highlight(highlight_time = 2)

    def test_click(self):
        self.pdriver.get("localhost:7777/click-test")

        element = self.pdriver.find("id:1")

        element.click()

        result = self.pdriver.find("xp://*[contains(text(), 'clicked')]")

        assert result != None

    def test_wait_until_visible(self):
        self.pdriver.get("localhost:7777/wait_until_visible-test")

        element = self.pdriver.find("id:2", raise_exception = False)
        assert element.get_attribute('id') == '2'

        element.highlight()

        element = self.pdriver.find("id:3", raise_exception = False)
        assert element == None

    def test_wait_until_not_visible(self):
        self.pdriver.get("localhost:7777/wait_until_not_visible-test")

        self.pdriver.wait_until_not_visible("id:2", raise_exception = False)

        element = self.pdriver.find("id:2", raise_exception = False)
        assert element == None

    def test_wait_until_not_visible_hidden(self):
        self.pdriver.get("localhost:7777/wait_until_not_visible-test")

        self.pdriver.wait_until_not_visible("id:4", raise_exception = False)

        element = self.pdriver.find("id:4", raise_exception = False)
        assert element == None

if __name__ == "__main__":
    unittest.main()
