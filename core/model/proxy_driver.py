#! -*- coding: utf-8 -*-

from inspect import currentframe

from brome.core.model.utils import *
from brome.core.model.test import Test
from brome.core.model.test_result import TestResult
from brome.core.model.proxy_element import ProxyElement
from brome.core.model.proxy_element_list import ProxyElementList

class ProxyDriver(object):

    def __init__(self, **kwargs):
        self._driver = kwargs.get('driver')
        self.test_instance = kwargs.get('test_instance')
        self.runner = kwargs.get('runner')

        self.brome = self.runner.brome
        self.selector_dict = self.brome.selector_dict
    
    def __getattr__(self, funcname):
        return getattr(self._driver, funcname)

    def find(self, selector, **kwargs):
        self.info_log("Finding element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)

        if len(elements):
            return elements[0]
        else:
            return None

    def find_last(self, selector, **kwargs):
        self.info_log("Finding last element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)

        if len(elements):
            return elements[-1]
        else:
            return None

    def find_all(self, selector, **kwargs):
        self.info_log("Finding elements with selector: %s"%selector)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.test_instance.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        wait_until_visible = kwargs.get(
                                        'wait_until_visible',
                                        self.test_instance.get_config_value(
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
            if not self.selector_dict.has_key(selector[3:]):
                raise Exception("Cannot find the selector variable (%s) in the selector dict"%selector[3:])

            selector_variable = self.selector_dict[selector[3:]]
            if type(selector_variable) == dict:
                if selector_variable.has_key(self.get_id()):
                    return self.selector_function_resolver(
                        selector_variable.get(self.get_id())
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

        self.debug_log('func: %s'%func)
        self.debug_log('effective_selector: %s'%effective_selector)

        return func, effective_selector

    def wait_until_visible(self, selector, **kwargs):
        self.info_log("Waiting until visible (%s)"%selector)
        
        timeout = kwargs.get(
                            'timeout',
                            int(self.test_instance.get_config_value(
                                'proxy_driver:default_timeout'
                            ))
                        )
        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.test_instance.get_config_value(
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
        self.info_log("Waiting until not visible (%s)"%selector)

        timeout = kwargs.get(
                            'timeout',
                            int(self.test_instance.get_config_value(
                                'proxy_driver:default_timeout'
                            ))
                        )
        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.test_instance.get_config_value(
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
        if self.test_instance.get_config_value("runner:play_sound_on_pdb"):
            say(self.test_instance.get_config_value("runner:sound_on_pdb"))

        set_trace()

    def embed(self, title = '', stack_depth = 2):
        from IPython.terminal.embed import InteractiveShellEmbed

        if self.test_instance.get_config_value("runner:play_sound_on_ipython_embed"):
            say(self.test_instance.get_config_value("runner:sound_on_ipython_embed"))

        ipshell = InteractiveShellEmbed(banner1 = title)

        frame = currentframe()
        for i in range(stack_depth - 1):
            frame = frame.f_back

        msg = 'Stopped at %s and line %s; stack_depth: %s'%(frame.f_code.co_filename, frame.f_lineno, stack_depth)

        ipshell(msg, stack_depth = stack_depth)

    def take_screenshot(self, screenshot_name = None, screenshot_path = None):
        self.info_log("Taking a screenshot...")

        if screenshot_path:
            self._driver.save_screenshot(screenshot_path)
            self.info_log("Screenshot taken (%s)"%screenshot_path)

        elif screenshot_name:
            take_screenshot = True
            if hasattr(self.runner, "screenshot_cache"):
                if self.runner.screenshot_cache.get(screenshot_name):
                    self.debug_log("screenshot(%s) found in cache"%screenshot_name)
                    take_screenshot = False

            if take_screenshot:
                screenshot_path = os.path.join(
                        self.test_instance._screenshot_dir,
                        '%s.png'%string_to_filename(screenshot_name)
                    )
                self._driver.save_screenshot(
                    screenshot_path
                )
                self.info_log("Screenshot taken (%s)"%screenshot_path)
        else:
            screenshot_path = os.path.join(
                    self.test_instance._screenshot_dir,
                    '%s.png'%get_timestamp()
                )
            self._driver.save_screenshot(
                screenshot_path
            )
            self.info_log("Screenshot taken (%s)"%screenshot_path)

    def assert_visible(self, selector, testid = False, **kwargs):
        self.info_log("Assert visible selector(%s) testid(%s)"%(selector, testid))

        element = self.find(selector, raise_exception = False)
        if element:
            self.create_test_result(testid, True)
        else:
            self.create_test_result(testid, False)

    def assert_not_visible(self, selector, testid = False, **kwargs):
        self.info_log("Assert not visible selector(%s) testid(%s)"%(selector, testid))

        element = self.find(selector, raise_exception = False)
        if element:
            self.create_test_result(testid, False)
        else:
            self.create_test_result(testid, True)

    def assert_text_equal(self, selector, value, testid = False, **kwargs):
        self.info_log("Assert text equal selector(%s) testid(%s)"%(selector, testid))

        element = self.find(selector, raise_exception = False)
        if element:
            if element.text == value:
                self.create_test_result(testid, True)
            else:
                self.create_test_result(testid, False)
        else:
            self.create_test_result(testid, False)

    def assert_text_not_equal(self, selector, value, testid = False, **kwargs):
        self.info_log("Assert text not equal selector(%s) testid(%s)"%(selector, testid))

        element = self.find(selector, raise_exception = False)
        if element:
            if element.text != value:
                self.create_test_result(testid, True)
            else:
                self.create_test_result(testid, False)
        else:
            self.create_test_result(testid, False)

    def create_test_result(self, testid, result, **kwargs):
        embed = True
        videocapture_path = ''
        extra_data = ''

        if not self.test_instance._session.query(Test).filter(Test.test_id == testid).count():
            test = None
        else:
            test = self.test_instance._session.query(Test).filter(Test.test_id == testid).one()

        if self.brome.test_dict.has_key(testid):
            test_config = self.brome.test_dict[testid]
            if type(test_config) == dict:
                if test_config.has_key('embed'):
                    embed = test_config['embed']
                    test_name = test_config['name']
            else:
                test_name = test_config
        else:
            test_name = testid

        if result:
            #SCREENSHOT
            if self.test_instance.get_config_value("proxy_driver:take_screenshot_on_assertion_success"):
                screenshot_name = 'succeed_%s_%s_%s.png'%(
                    string_to_filename(testid),
                    get_timestamp(),
                    self.get_id(join_char = '_')
                )
                screenshot_path = os.path.join(
                    self.test_instance._assertion_screenshot_dir,
                    screenshot_name
                )
                self.take_screenshot(screenshot_path = screenshot_path)

            #SOUND NOTIFICATION
            if self.test_instance.get_config_value("runner:play_sound_on_assertion_success"):
                say(self.test_instance.get_config_value("runner:sound_on_assertion_success").format(testid = testid))

            #EMBED
            if self.test_instance.get_config_value("runner:embed_on_assertion_success") and embed:
                self.embed(title = test_name)
        else:
            #SCREENSHOT
            if self.test_instance.get_config_value("proxy_driver:take_screenshot_on_assertion_success"):
                screenshot_name = 'failed_%s_%s_%s.png'%(
                    string_to_filename(testid),
                    get_timestamp(),
                    self.get_id(join_char = '_')
                )
                screenshot_path = os.path.join(
                    self.test_instance._assertion_screenshot_dir,
                    screenshot_name
                )
                self.take_screenshot(screenshot_path = screenshot_path)

            #SOUND NOTIFICATION
            if self.test_instance.get_config_value("runner:play_sound_on_assertion_failure"):
                say(self.test_instance.get_config_value("runner:sound_on_assertion_failure").format(testid = testid))

            #EMBED
            if self.test_instance.get_config_value("runner:embed_on_assertion_failure") and embed:
                self.embed(title = test_name)

        test_result = TestResult(
            result = result,
            timestamp = datetime.now(),
            browser_id = self.get_id(),
            screenshot_path = screenshot_path,
            videocapture_path = videocapture_path,
            extra_data = extra_data,
            title = test_name,
            test = test,
            testinstance = self.test_instance._sa_test_instance,
            testbatch = self.runner.sa_test_batch
        )
        self.test_instance._session.add(test_result)
        self.test_instance._session.commit()

    def debug_log(self, msg):
        self.test_instance.debug_log(msg)

    def info_log(self, msg):
        self.test_instance.info_log(msg)

    def warning_log(self, msg):
        self.test_instance.warning_log(msg)

    def error_log(self, msg):
        self.test_instance.error_log(msg)

    def critical_log(self, msg):
        self.test_instance.critial_log(msg)

    def configure_resolution(self):
        #Maximaze window
        if self.test_instance.get_config_value('browser:maximize_window'):
            self._driver.maximize_window()
        else:
            #Window position
            self._driver.set_window_position(
                self.test_instance.get_config_value('browser:window_x_position'),
                self.test_instance.get_config_value('browser:window_y_position')
            )

            #Window size
            self._driver.set_window_size(
                self.test_instance.get_config_value('browser:window_width'),
                self.test_instance.get_config_value('browser:window_height')
            )

    def get_id(self, join_char = '-'):
        return join_char.join([
                    self.get_browser_name(),
                    self.get_browser_version(),
                    self.get_platform()
                ])

    def get_browser_name(self):
        return self._driver.capabilities['browserName']

    def get_browser_version(self):
        return self._driver.capabilities['version'].replace('.', '_')

    def get_platform(self):
        return self._driver.capabilities['platform'].replace('.', '_')
