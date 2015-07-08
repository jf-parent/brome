
from brome import *
from brome.core.model.proxy_element import ProxyElement
from brome.core.model.proxy_element_list import ProxyElementList

class ProxyDriver(object):

    def __init__(self, driver, browser_instance, selector_dict):
        self._driver = driver
        self.browser_instance = browser_instance
        self.selector_dict = selector_dict
    
    def __getattr__(self, funcname):
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
        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.browser_instance.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        wait_until_visible = kwargs.get(
                                        'wait_until_visible',
                                        self.browser_instance.get_config_value(
                                            'proxy_driver:wait_until_visible_before_find'
                                        )
                                    )

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
            if not self.selector_dict:
                raise Exception("No selector dict given to the brome-execute")

            selector_variable = self.selector_dict[selector[3:]]
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

        self.browser_instance.debug_log('func: %s'%func)
        self.browser_instance.debug_log('effective_selector: %s'%effective_selector)
        return func, effective_selector

    def wait_until_visible(self, selector, **kwargs):
        timeout = kwargs.get(
                            'timeout',
                            int(self.browser_instance.get_config_value(
                                'proxy_driver:default_timeout'
                            ))
                        )
        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.browser_instance.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )

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
        timeout = kwargs.get(
                            'timeout',
                            int(self.browser_instance.get_config_value(
                                'proxy_driver:default_timeout'
                            ))
                        )
        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.browser_instance.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )

        func, effective_selector = self.selector_function_resolver(selector, function_type = 'by')

        try:
            WebDriverWait(self._driver, timeout).until(EC.invisibility_of_element_located((getattr(By, func), effective_selector[3:])))
            return True
        except TimeoutException:
            if raise_exception:
                raise TimeoutException(selector)
            else:
                return False

    def pdb(self):
        from pudb import set_trace
        from bdb import BdbQuit

        if self.browser_instance.get_config_value("runner:play_sound_on_pdb"):
            say(self.browser_instance.get_config_value("runner:sound_on_pdb"))

        try:
            set_trace()
        except BdbQuit:
            pass

    def embed(self, title, stack_depth = 2):
        from IPython.terminal.embed import InteractiveShellEmbed

        if self.browser_instance.get_config_value("runner:play_sound_on_ipython_embed"):
            say(self.browser_instance.get_config_value("runner:sound_on_ipython_embed"))

        ipshell = InteractiveShellEmbed(banner1 = note)

        frame = currentframe()
        for i in range(stack_depth - 1):
            frame = frame.f_back

        msg = 'Stopped at %s and line %s; stack_depth: %s'%(frame.f_code.co_filename, frame.f_lineno, stack_depth)

        ipshell(msg, stack_depth = stack_depth)
