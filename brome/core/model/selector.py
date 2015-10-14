#! -*- coding: utf-8 -*-

import re
from StringIO import StringIO

from lxml import etree
from lxml.cssselect import CSSSelector
from cssselect.parser import SelectorSyntaxError

class Selector(object):
    """Selector class to manage the selector brome system

    Args:
        pdriver (object)
        selector (str)
    """
    def __init__(self, pdriver, selector):
        self._pdriver = pdriver
        self._selector = selector

        #List of selector support
        if not type(selector) is list:
            self._selector_list= [self._selector]
        else:
            self._selector_list = self._selector

        self._effective_selector_list = self.resolve_selector()
        self._effective_selector_type = self.resolve_selector_type()

        self.find_function, self.find_by = self.resolve_function()

        self._effective_selector = ''.join([self._get_selector(sel) for sel in self._effective_selector_list])

        #XPATH VALIDATION
        if self._effective_selector_type == 'xpath':
            if self._pdriver.get_config_value("proxy_driver:validate_xpath_selector"):
                xpath_test = etree.parse(StringIO('<foo><bar></bar></foo>'))
                try:
                    xpath_test.xpath(self.get_selector())
                except etree.XPathEvalError, e:
                    raise Exception("Invalid xpath: %s"%self.get_selector())

        #CSS VALIDATION
        elif self._effective_selector_type == 'css':
            if self._pdriver.get_config_value("proxy_driver:validate_css_selector"):
                try:
                    CSSSelector(self.get_selector())
                except SelectorSyntaxError:
                    raise Exception("Invalid css selector: %s"%self.get_selector())

    def __repr__(self):
        return "Selector: effective selector (%s), raw selector (%s)"%(self.get_selector(), self._selector)

    #GET
    def get_selector(self):
        """Get the final selector

        This selector can be feed to selenium
        """
        return self._effective_selector

    def _get_selector(self, selector):
        """Get the selector without his brome specific prefix
        """
        return selector[3:]

    def get_type(self, selector):
        """Get the type of the selector

        see SELECTOR_DICT for supported type
        """
        try:
            return SELECTOR_DICT[selector[:3]]
        except KeyError:
            raise Exception("""
                All selector need to start with either:
                    'nm:' (name), 'xp:' (xpath), 'cn:' (classname), 'id:' (id), 'cs:' (css), 'tn:' (tag name), 'lt:' (link text), 'pl:' (partial link text)
            """)

    #RESOLVE
    def resolve_selector(self):
        """Resolve the selector variable in place
        """
        effective_selector_list = []

        for current_selector in self._selector_list:

            #INLINE SELECTOR
            if self.get_type(current_selector) != 'selector_variable':
                effective_selector_list.append(current_selector)

            #SELECTOR VARIABLE
            else:
                #Make sure the proxy driver have a selector dictionary
                if self.get_type(current_selector) == 'selector_variable':
                    if not hasattr(self._pdriver, 'selector_dict'):
                        raise Exception("You must provide a selector dictionary if you want to use the selector variable type")

                #Make sure that the selector dictionary contains the selector variable
                if not self._pdriver.selector_dict.has_key(self._get_selector(current_selector)):
                    raise Exception("Cannot find the selector variable (%s) in the selector dictionary"%self._get_selector(current_selector))

                effective_selector = self._pdriver.selector_dict[self._get_selector(current_selector)]
                if type(effective_selector) is dict:
                    current_browser_id = False

                    keys = [key for key in effective_selector.keys() if key != 'default']
                    for key in keys:
                        for target in key.split('|'):
                            try:
                                re.search(target, self._pdriver.get_id()).group(0)
                                current_browser_id = key
                            except AttributeError:
                                pass

                    if current_browser_id:
                        effective_selector_list.append(effective_selector.get(current_browser_id))
                    else:
                        effective_selector_list.append(effective_selector.get('default'))

                else:
                    if self.get_type(effective_selector) in [value for key,value in SELECTOR_DICT.items() if key != 'selector_variable']:
                        effective_selector_list.append(effective_selector)
                    else:
                        raise Exception("""
                            All selector need to start with either:
                                'nm:' (name), 'xp:' (xpath), 'cn:' (classname), 'id:' (id), 'cs:' (css), 'tn:' (tag name), 'lt:' (link text), 'pl:' (partial link text)
                        """)

        return effective_selector_list

    def resolve_selector_type(self):
        """Resolve the selector type

        This make sure that all the selectors provided are of the same type (in case of a list of selector)
        """
        resolved_selector_type_list = []
        for current_selector in self._effective_selector_list:
            resolved_selector_type_list.append(self.get_type(current_selector))

        set_ = set(resolved_selector_type_list)

        #VALIDATE THAT ALL SELECTOR ARE OF THE SAME TYPE
        if len(set_) != 1:
            raise Exception("If you provide a list of selector then all selectors must be of the same type")
        else:
            return set_.pop()

    def resolve_function(self):
        """Resolve the selenium function that will be use to find the element
        """
        selector_type = self._effective_selector_type

        #NAME
        if selector_type == 'name':
            return ('find_elements_by_name', 'NAME')

        #XPATH
        elif selector_type == 'xpath':
            return ('find_elements_by_xpath', 'XPATH')

        #CLASSNAME
        elif selector_type == 'class_name':
            return ('find_elements_by_class_name', 'CLASS_NAME')

        #ID
        elif selector_type == 'id':
            return ('find_element_by_id', 'ID')

        #CSS
        elif selector_type == 'css':
            return ('find_elements_by_css_selector', 'CSS_SELECTOR')

        #TAGNAME
        elif selector_type == 'tag_name':
            return ('find_elements_by_tag_name', 'TAG_NAME')

        #LINK TEXT
        elif selector_type == 'link_text':
            return ('find_elements_by_link_text', 'LINK_TEXT')

        #PARTIAL LINK TEXT
        elif selector_type == 'partial_link_text':
            return ('find_elements_by_partial_link_text', 'PARTIAL_LINK_TEXT')

SELECTOR_DICT = {
    'nm:': 'name',
    'xp:': 'xpath',
    'lt:': 'link_text',
    'pl:': 'partial_link_text',
    'cn:': 'class_name',
    'id:': 'id',
    'cs:': 'css',
    'tn:': 'tag_name',
    'sv:': 'selector_variable'
}
