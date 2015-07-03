
from brome.core.models.proxy_element import ProxyElement
from brome.core.models.utils import selector_function_resolver
from brome.core.models.proxy_element_list import ProxyElementList

class ProxyDriver(object):

    def __init__(self, driver):
        self._driver = driver
    
    def __getattr__(self, funcname):
        print 'proxydriver'
        return getattr(self._driver, funcname)

    def get_first(self, selector):
        func, effective_selector = selector_function_resolver(selector)

        element = getattr(self._driver, func)(effective_selector[3:])[0]

        return ProxyElement(element)

    def get_last(self, selector):
        func, effective_selector = selector_function_resolver(selector)

        element = getattr(self._driver, func)(effective_selector[3:])[-1]

        return ProxyElement(element)

    def get_all(self, selector):
        func, effective_selector = selector_function_resolver(selector)

        elements = getattr(self._driver, func)(effective_selector[3:])

        return ProxyElementList(elements)
