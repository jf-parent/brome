
from brome import config
from brome.core.models.utils import *
from brome.core.models.proxy_element import ProxyElement
from brome.core.models.proxy_element_list import ProxyElementList
from brome.core.runner.base_browser_instance import BaseBrowserInstance

class ProxyDriver(object):

    def __init__(self, driver):
        self._driver = driver
        self.browser_instance = BaseBrowserInstance(self)
    
    def __getattr__(self, funcname):
        print 'proxydriver'
        return getattr(self._driver, funcname)

    def find(self, selector, **kwargs):
        elements = self.find_all(selector, **kwargs)

        if len(elements):
            return elements[0]
        else:
            return None

    def find_last(self, selector, **kwargs):
        elements = self.find_all(selector, **kwargs)

        if len(elements):
            return elements[-1]
        else:
            return None

    def find_all(self, selector, **kwargs):
        """
            raise_exception: bool; default: true
            wait_until_visible: bool; default: true
        """
        raise_exception = kwargs.get('raise_exception', True)
        wait_until_visible = kwargs.get('wait_until_visible', True)

        func, effective_selector = self.selector_function_resolver(selector)

        if wait_until_visible:
            ret = self.wait_until_visible(selector, raise_exception = raise_exception)
            if not ret:
                return []

        try:
            elements = getattr(self._driver, func)(effective_selector[3:])
        except NoSuchElementException:
            if raise_exception:
                raise NoSuchElementException(effective_selector)
            else:
                return []

        if type(elements) == list:
            if len(elements):
                return ProxyElementList(elements, selector)
            else:
                if raise_exception:
                    raise NoSuchElementException(effective_selector)
                else:
                    return []
        else:
            return [ProxyElement(elements, selector)]

    def selector_function_resolver(self, selector, **kwargs):
        """
            kwargs:
                function_type: 'by' | 'find_by'; default: 'find_by'
        """

        function_type = kwargs.get('function_type', 'find_by')

        selector_type = selector[0:2]
        effective_selector = selector

        if selector_type == 'nm':
            if function_type == 'find_by':
                func = 'find_elements_by_name'
            elif 'by':
                func = 'NAME'

        elif selector_type == 'xp':
            if function_type == 'find_by':
                func = 'find_elements_by_xpath'
            elif 'by':
                func = 'XPATH'

        elif selector_type == 'cn':
            if function_type == 'find_by':
                func = 'find_elements_by_class_name'
            elif 'by':
                func = 'CLASS_NAME'

        elif selector_type == 'id':
            if function_type == 'find_by':
                func = 'find_element_by_id'
            elif 'by':
                func = 'ID'

        elif selector_type == 'cs':
            if function_type == 'find_by':
                func = 'find_elements_by_css_selector'
            elif 'by':
                func = 'CSS_SELECTOR'

        elif selector_type == 'tn':
            if function_type == 'find_by':
                func = 'find_elements_by_tag_name'
            elif 'by':
                func = 'TAG_NAME'

        elif selector_type == 'lt':
            if function_type == 'find_by':
                func = 'find_elements_by_link_text'
            elif 'by':
                func = 'LINK_TEXT'

        elif selector_type == 'pl':
            if function_type == 'find_by':
                func = 'find_elements_by_partial_link_text'
            elif 'by':
                func = 'PARTIAL_LINK_TEXT'

        elif selector_type == 'sv':
            selector_variable = config['selector_variable_dict'][selector[3:]]
            if type(selector_variable) == dict:
                if selector_variable.has_key(self.browser_instance.get_id()):
                    return self.selector_function_resolver(
                        selector_variable.get(self.browser_instance.get_id())
                    )
                else:
                    return self.selector_function_resolver(selector_variable.get('default'))
            else:
                return self.selector_function_resolver(selector_variable)

        else:
            raise Exception("""
                Cannot resolve selector function name! All selector need to start with either:
                    'nm:' (name), 'xp:' (xpath), 'cn:' (classname), 'id:' (id), 'cs:' (css), 'tn:' (tag name), 'lt:' (link text), 'pl:' (partial link text)
            """)

        print 'func', func
        print 'effective_selector', effective_selector
        return func, effective_selector

    def wait_until_visible(self, selector, **kwargs):
        """
            kwargs:
                timeout = int; default: 5
        """
        
        timeout = kwargs.get('timeout', 5)
        raise_exception = kwargs.get('raise_exception', True)

        func, effective_selector = self.selector_function_resolver(selector, function_type = 'by')

        try:
            WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located((getattr(By, func), effective_selector[3:])))
            return True
        except TimeoutException:
            if raise_exception:
                raise TimeoutException(selector)
            else:
                return False

    def wait_until_not_visible(self, selector, **kwargs):
        """
            kwargs:
                timeout = int; default: 5
        """
        
        timeout = kwargs.get('timeout', 5)
        raise_exception = kwargs.get('raise_exception', True)

        func, effective_selector = self.selector_function_resolver(selector, function_type = 'by')

        try:
            WebDriverWait(self._driver, timeout).until(EC.invisibility_of_element_located((getattr(By, func), effective_selector[3:])))
            return True
        except TimeoutException:
            if raise_exception:
                raise TimeoutException(selector)
            else:
                return False
