#! -*- coding: utf-8 -*-

from inspect import currentframe, getframeinfo
import re

from brome.core.model.utils import *
from brome.core.model.meta.base import Session
from brome.core.model.selector import Selector
from brome.core.model.test import Test
from brome.core.model.test_result import TestResult
from brome.core.model.proxy_element import ProxyElement
from brome.core.model.proxy_element_list import ProxyElementList

class ProxyDriver(object):

    def __init__(self, **kwargs):
        self._driver = kwargs.get('driver')
        self.test_instance = kwargs.get('test_instance')
        self.runner = kwargs.get('runner')

        self.browser_config = self.test_instance._browser_config
        self.brome = self.runner.brome
        self.selector_dict = self.brome.selector_dict

        self.embed_disabled = False

        self.no_javascript_error_string = 'No javascript error'
    
    def __getattr__(self, funcname):
        return getattr(self._driver, funcname)

    def get(self, url):
        self._driver.get(url)

        if self.get_config_value("proxy_driver:intercept_javascript_error"):
            self.init_javascript_error_interception()
        
        return True

    def init_javascript_error_interception(self):
        self.debug_log("Initializing javascript error interception")

        self._driver.execute_script("""
            window.jsErrors = [];
            window.onerror = function (errorMessage, url, lineNumber) {
                var message = 'Error: ' + errorMessage;
                window.jsErrors.push(message);
                return false;
            };
        """)

    def print_javascript_error(self, **kwargs):
        errors = self.get_javascript_error(return_type = 'list')
        if errors:
            self.info_log("Javascript error:")
            for error in errors:
                self.info_log(error)

    def get_javascript_error(self, **kwargs):
        """
            kwargs:
                return_type: 'string' | 'list'; default: 'string'
        """
        
        return_type = kwargs.get('return_type', 'string')

        js_errors = []
        if self.get_config_value("proxy_driver:intercept_javascript_error"):
            js_errors = self._driver.execute_script('return window.jsErrors; window.jsErrors = [];')

            if not js_errors:
                js_errors = []

            if return_type == 'list':
                if len(js_errors):
                    return js_errors
                else:
                    return []
            else:
                if len(js_errors):
                    return '\n'.join(js_errors)
                else:
                    return self.no_javascript_error_string
        else:
            self.warning_log("get_javascript_error was call but proxy_driver:intercept_javascript_error is set to False")
            return []

    #IS
    def is_present(self, selector, **kwargs):
        self.debug_log(u"Is present (%s)"%selector)
        
        element = self.find(
            selector,
            raise_exception = False,
            wait_until_present = False,
            wait_until_visible = False
        )
        if element:
            self.debug_log("is present: True")
            return True
        else:
            self.debug_log("is present: False")
            return False

    def is_visible(self, selector, **kwargs):
        self.debug_log(u"Is visible (%s)"%selector)

        element = self.find(
            selector,
            raise_exception = False,
            wait_until_present = False,
            wait_until_visible = False
        )

        if element:
            if element.is_displayed(raise_exception = False):

                element.highlight(
                    style = self.get_config_value(
                                'highlight:element_is_visible'
                            )
                )

                self.debug_log(u"is visible (%s): True"%selector)

                return True

        self.debug_log(u"is visible (%s): False"%selector)

        return False

    #FIND
    def find(self, selector, **kwargs):
        self.debug_log(u"Finding element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)

        if len(elements):
            self.debug_log(u"find (%s): Element found"%(selector))
            return elements[0]
        else:
            self.debug_log(u"find (%s): No element found"%(selector))
            return None

    def find_last(self, selector, **kwargs):
        self.debug_log(u"Finding last element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)

        if len(elements):
            self.debug_log(u"find_last (%s): element found"%selector)
            return elements[-1]
        else:
            self.debug_log(u"find_last (%s): No element found"%selector)
            return None

    def find_all(self, selector, **kwargs):
        self.debug_log(u"Finding elements with selector: %s"%selector)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        wait_until_present = kwargs.get(
                                        'wait_until_present',
                                        self.get_config_value(
                                            'proxy_driver:wait_until_present_before_find'
                                        )
                                    )
        self.debug_log(u"effective wait_until_present: %s"%wait_until_present)

        wait_until_visible = kwargs.get(
                                        'wait_until_visible',
                                        self.get_config_value(
                                            'proxy_driver:wait_until_visible_before_find'
                                        )
                                    )
        self.debug_log(u"effective wait_until_visible: %s"%wait_until_visible)

        _selector = Selector(self, selector)

        found = False 
        if wait_until_visible:
            #we don't raise exception here otherwise none visible element will always raise exception
            #TODO find a good way to make it configurable
            found = self.wait_until_visible(selector, raise_exception = False)

        if wait_until_present and not found:
            found = self.wait_until_present(selector, raise_exception = raise_exception)
            if not found:
                self.debug_log(u"find_all (%s): No element found"%_selector)
                return []

        try:
            elements = getattr(self._driver, _selector.find_function)(_selector.get_selector())
        except NoSuchElementException:
            self.debug_log(u"find_all (%s): No element found"%_selector)
            self.print_javascript_error()
            if raise_exception:
                raise NoSuchElementException(_selector)
            else:
                return []

        if type(elements) == list:
            if len(elements):
                self.debug_log(u"find_all (%s): Element found"%_selector)
                return ProxyElementList(elements, selector, self)
            else:
                msg = u"find_all (%s): No element found"%_selector
                self.debug_log(msg)
                self.print_javascript_error()
                if raise_exception:
                    raise NoSuchElementException(msg)
                else:
                    return []
        else:
            self.debug_log(u"find_all (%s): Element found"%_selector)
            return [ProxyElement(elements, selector, self)]

    #WAIT
    def wait_until_clickable(self, selector, **kwargs):
        self.info_log("Waiting until clickable (%s)"%selector)
        
        timeout = kwargs.get(
                            'timeout',
                            self.get_config_value(
                                'proxy_driver:default_timeout'
                            )
                        )
        self.debug_log(u"effective timeout: %s"%timeout)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        _selector = Selector(self, selector)

        try:
            WebDriverWait(self._driver, timeout).until(EC.element_to_be_clickable((getattr(By, _selector.fin_by), _selector.get_selector())))
            self.debug_log(u"wait_until_clickable (%s): element is clickable"%_selector)
            return True
        except TimeoutException:
            msg = u"wait_until_clickable: element (%s) is still not clickable"%_selector
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                raise TimeoutException(msg)
            else:
                return False

    def wait_until_present(self, selector, **kwargs):
        self.info_log("Waiting until present (%s)"%selector)
        
        timeout = kwargs.get(
                            'timeout',
                            self.get_config_value(
                                'proxy_driver:default_timeout'
                            )
                        )
        self.debug_log(u"effective timeout: %s"%timeout)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        _selector = Selector(self, selector)
        try:
            el = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((getattr(By, _selector.find_by), _selector.get_selector())))
            self.debug_log(u"wait_until_present (%s): element is present"%_selector)
            return ProxyElement(el, selector, self)
        except TimeoutException:
            msg = u"wait_until_present (%s): element is still not present"%_selector
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                raise TimeoutException(msg)
            else:
                return False

    def wait_until_not_present(self, selector, **kwargs):
        self.info_log("Waiting until not present (%s)"%selector)
        
        timeout = kwargs.get(
                            'timeout',
                            self.get_config_value(
                                'proxy_driver:default_timeout'
                            )
                        )
        self.debug_log(u"effective timeout: %s"%timeout)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        _selector = Selector(self, selector)
        try:
            WebDriverWait(self._driver, timeout).until(EC.invisibility_of_element_located((getattr(By, _selector.find_by), _selector.get_selector())))
            self.debug_log(u"wait_until_not_present (%s): element is not present"%_selector)
            return True
        except TimeoutException:
            msg = u"wait_until_not_present (%s): element is still present"%_selector
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                raise TimeoutException(msg)
            else:
                return False

    def wait_until_visible(self, selector, **kwargs):
        self.info_log("Waiting until visible (%s)"%selector)
        
        timeout = kwargs.get(
                            'timeout',
                            self.get_config_value(
                                'proxy_driver:default_timeout'
                            )
                        )
        self.debug_log(u"effective timeout: %s"%timeout)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        _selector = Selector(self, selector)
        try:
            el = WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located((getattr(By, _selector.find_by), _selector.get_selector())))
            self.debug_log(u"wait_until_visible (%s): element is visible"%_selector)
            return ProxyElement(el, selector, self)
        except TimeoutException:
            msg = u"wait_until_visible (%s): element is still not visible"%_selector
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                raise TimeoutException(msg)
            else:
                return False

    def wait_until_not_visible(self, selector, **kwargs):
        self.info_log("Waiting until not visible (%s)"%selector)

        timeout = kwargs.get(
                            'timeout',
                            self.get_config_value(
                                'proxy_driver:default_timeout'
                            )
                        )
        self.debug_log(u"effective timeout: %s"%timeout)

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        self.debug_log(u"effective raise_exception: %s"%raise_exception)

        _selector = Selector(self, selector)
        try:
            WebDriverWait(self._driver, timeout).until(EC.invisibility_of_element_located((getattr(By, _selector.find_by), _selector.get_selector())))
            self.debug_log(u"wait_until_not_visible (%s): element is not visible"%_selector)
            return True
        except TimeoutException:
            msg = u"wait_until_not_visible (%s): element is still visible"%_selector
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                raise TimeoutException(msg)
            else:
                return False

    def pdb(self):
        if self.get_config_value("runner:play_sound_on_pdb"):
            say(self.get_config_value("runner:sound_on_pdb"))

        set_trace()

    def embed(self, title = ''):
        if self.embed_disabled:
            self.warning_log("Embed are disabled when runned from the grid runner because of the multithreading")
            return False
            
        from IPython.terminal.embed import InteractiveShellEmbed

        if self.get_config_value("runner:play_sound_on_ipython_embed"):
            say(self.get_config_value("runner:sound_on_ipython_embed"))

        ipshell = InteractiveShellEmbed(banner1 = title)

        frame = currentframe()
        stack_depth = 1
        for i in range(5):
            frame = frame.f_back
            stack_depth += 1
            if not frame.f_code.co_filename in __file__:
                break

        msg = 'Stopped at %s and line %s;'%(frame.f_code.co_filename, frame.f_lineno)

        ipshell(msg, stack_depth = stack_depth)

    def take_screenshot(self, screenshot_name = None, screenshot_path = None):
        self.info_log("Taking a screenshot...")

        if screenshot_path:
            self._driver.save_screenshot(screenshot_path)
            self.debug_log(u"Screenshot taken (%s)"%screenshot_path)

        elif screenshot_name:
            take_screenshot = True
            if hasattr(self.runner, "screenshot_cache"):
                if self.runner.screenshot_cache.get(screenshot_name):
                    self.debug_log(u"screenshot(%s) found in cache"%screenshot_name)
                    take_screenshot = False

            if take_screenshot:
                screenshot_path = os.path.join(
                        self.test_instance._screenshot_dir,
                        '%s.png'%string_to_filename(screenshot_name)
                    )
                self._driver.save_screenshot(
                    screenshot_path
                )
                self.debug_log(u"Screenshot taken (%s)"%screenshot_path)
        else:
            screenshot_path = os.path.join(
                    self.test_instance._screenshot_dir,
                    '%s.png'%get_timestamp()
                )
            self._driver.save_screenshot(
                screenshot_path
            )
            self.debug_log(u"Screenshot taken (%s)"%screenshot_path)

    #ASSERT
    def assert_present(self, selector, testid = None, **kwargs):
        self.info_log("Assert present selector(%s) testid(%s)"%(selector, testid))

        wait_until_present = kwargs.get('wait_until_present',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_present_before_assert_present'
                                    )
                                )
        self.debug_log(u"effective wait_until_present: %s"%wait_until_present)

        if wait_until_present:
            element = self.wait_until_present(selector, raise_exception = False)
        else:
            element = self.is_present(selector)

        if element:
            if testid is not None:
                self.create_test_result(testid, True)

            return True
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_not_present(self, selector, testid = None, **kwargs):
        self.info_log("Assert not present selector(%s) testid(%s)"%(selector, testid))

        wait_until_not_present = kwargs.get('wait_until_not_present',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_not_present_before_assert_not_present'
                                    )
                                )
        self.debug_log(u"effective wait_until_not_present: %s"%wait_until_not_present)

        if wait_until_not_present:
            ret = self.wait_until_not_present(selector, raise_exception = False)
        else:
            ret = not self.is_present(selector)

        if ret:
            if testid is not None:
                self.create_test_result(testid, True)

            return True
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_visible(self, selector, testid = None, **kwargs):
        self.info_log("Assert visible selector(%s) testid(%s)"%(selector, testid))

        highlight = kwargs.get('highlight',
                                self.get_config_value(
                                    'highlight:highlight_on_assertion_success'
                                )
                            )
        self.debug_log(u"effective highlight: %s"%highlight)

        wait_until_visible = kwargs.get('wait_until_visible',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_visible_before_assert_visible'
                                    )
                                )
        self.debug_log(u"effective wait_until_visible: %s"%wait_until_visible)

        if wait_until_visible:
            self.wait_until_visible(selector, raise_exception = False)

        element = self.find(selector, raise_exception = False, wait_until_visible = False, wait_until_present = False)
        if element and element.is_displayed(raise_exception = False):
            if highlight:
                element.highlight(
                    style = self.get_config_value(
                                'highlight:on_assertion_success'
                            )
                )
            if testid is not None:
                self.create_test_result(testid, True)

            return True
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_not_visible(self, selector, testid = None, **kwargs):
        self.info_log("Assert not visible selector(%s) testid(%s)"%(selector, testid))

        highlight = kwargs.get('highlight',
                                self.get_config_value(
                                    'highlight:highlight_on_assertion_failure'
                                )
                            )
        self.debug_log(u"effective highlight: %s"%highlight)

        wait_until_not_visible = kwargs.get('wait_until_not_visible',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_not_visible_before_assert_not_visible'
                                    )
                                )
        self.debug_log(u"effective wait_until_not_visible: %s"%wait_until_not_visible)

        if wait_until_not_visible:
            self.wait_until_not_visible(selector, raise_exception = False)

        element = self.find(selector, raise_exception = False, wait_until_visible = False, wait_until_present = False)
        if element and element.is_displayed(raise_exception = False):
            if highlight:
                element.highlight(
                    style = self.get_config_value(
                                'highlight:style_on_assertion_failure'
                            )
                )
            if testid is not None:
                self.create_test_result(testid, False)

            return False
        else:
            if testid is not None:
                self.create_test_result(testid, True)
            
            return True

    def assert_text_equal(self, selector, value, testid = None, **kwargs):
        self.info_log("Assert text equal selector(%s) testid(%s)"%(selector, testid))

        highlight = kwargs.get('highlight',
                                self.get_config_value(
                                    'highlight:highlight_on_assertion_success'
                                )
                            )
        self.debug_log(u"effective highlight: %s"%highlight)

        wait_until_visible = kwargs.get('wait_until_visible',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_visible_before_assert_visible'
                                    )
                                )
        self.debug_log(u"effective wait_until_visible: %s"%wait_until_visible)

        element = self.find(selector, raise_exception = False, wait_until_visible = wait_until_visible)
        if element:
            if element.text == value:
                if highlight:
                    element.highlight(
                        style = self.get_config_value(
                                    'highlight:style_on_assertion_success'
                                )
                    )
                if testid is not None:
                    self.create_test_result(testid, True)

                return True
            else:
                if highlight:
                    element.highlight(
                        style = self.get_config_value(
                                    'highlight:style_on_assertion_failure'
                                )
                    )
                if testid is not None:
                    self.create_test_result(testid, False)

                return False
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_text_not_equal(self, selector, value, testid = None, **kwargs):
        self.info_log("Assert text not equal selector(%s) testid(%s)"%(selector, testid))

        highlight = kwargs.get('highlight',
                                self.get_config_value(
                                    'highlight:highlight_on_assertion_success'
                                )
                            )
        self.debug_log(u"effective highlight: %s"%highlight)

        wait_until_visible = kwargs.get('wait_until_visible',
                                    self.get_config_value(
                                        'proxy_driver:wait_until_visible_before_assert_visible'
                                    )
                                )
        self.debug_log(u"effective wait_until_visible: %s"%wait_until_visible)

        element = self.find(selector, raise_exception = False, wait_until_visible = wait_until_visible)
        if element:
            if element.text != value:
                if highlight:
                    element.highlight(
                        style = self.get_config_value(
                                    'highlight:style_on_assertion_success'
                                )
                    )
                if testid is not None:
                    self.create_test_result(testid, True)

                return True
            else:
                if highlight:
                    element.highlight(
                        style = self.get_config_value(
                                    'highlight:style_on_assertion_failure'
                                )
                    )
                if testid is not None:
                    self.create_test_result(testid, False)

                return False
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def create_test_result(self, testid, result, **kwargs):
        embed = True
        videocapture_path = ''
        screenshot_relative_path = ''
        extra_data = ''

        session = Session()

        if not session.query(Test).filter(Test.test_id == testid).count():
            test = None
        else:
            test = session.query(Test).filter(Test.test_id == testid).one()

        if self.brome.test_dict.has_key(testid):
            test_config = self.brome.test_dict[testid]
            if type(test_config) == dict:
                if test_config.has_key('embed'):
                    embed = test_config['embed']
                    test_name = test_config['name']
            else:
                test_name = test_config

            embed_title = '[%s] %s'%(testid, test_name)
        else:
            test_name = testid
            embed_title = test_name

        if result:
            #SCREENSHOT
            if self.get_config_value("proxy_driver:take_screenshot_on_assertion_success"):
                screenshot_name = 'succeed_%s_%s_%s.png'%(
                    string_to_filename(testid),
                    get_timestamp(),
                    self.get_id(join_char = '_')
                )
                screenshot_path = os.path.join(
                    self.test_instance._assertion_screenshot_dir,
                    screenshot_name
                )
                screenshot_relative_path = os.path.join(
                    self.test_instance._assertion_screenshot_relative_dir,
                    screenshot_name
                )
                self.take_screenshot(screenshot_path = screenshot_path)

            #SOUND NOTIFICATION
            if self.get_config_value("runner:play_sound_on_assertion_success"):
                say(self.get_config_value("runner:sound_on_assertion_success").format(testid = testid))

            #EMBED
            if self.get_config_value("runner:embed_on_assertion_success") and embed:
                self.embed(title = embed_title)
        else:
            #SCREENSHOT
            if self.get_config_value("proxy_driver:take_screenshot_on_assertion_failure"):
                screenshot_name = 'failed_%s_%s_%s.png'%(
                    string_to_filename(testid),
                    get_timestamp(),
                    self.get_id(join_char = '_')
                )
                screenshot_path = os.path.join(
                    self.test_instance._assertion_screenshot_dir,
                    screenshot_name
                )
                screenshot_relative_path = os.path.join(
                    self.test_instance._assertion_screenshot_relative_dir,
                    screenshot_name
                )
                self.take_screenshot(screenshot_path = screenshot_path)

            #SOUND NOTIFICATION
            if self.get_config_value("runner:play_sound_on_assertion_failure"):
                say(self.get_config_value("runner:sound_on_assertion_failure").format(testid = testid))

            #EMBED
            if self.get_config_value("runner:embed_on_assertion_failure") and embed:
                self.embed(title = embed_title)

        sa_test_result = TestResult(
            result = result,
            timestamp = datetime.now(),
            browser_id = self.get_id(),
            screenshot_path = screenshot_relative_path,
            videocapture_path = videocapture_path,
            extra_data = extra_data,
            title = test_name,
            test = test,
            test_instance_id = self.test_instance.test_instance_id,
            test_batch_id = self.runner.test_batch_id
        )
        session.add(sa_test_result)
        session.commit()
        session.close()

    #LOG
    def debug_log(self, msg):
        self.test_instance.debug_log(msg)

    def info_log(self, msg):
        self.test_instance.info_log(msg)

    def warning_log(self, msg):
        self.test_instance.warning_log(msg)

    def error_log(self, msg):
        self.test_instance.error_log(msg)

    def critical_log(self, msg):
        self.test_instance.critical_log(msg)

    def configure_resolution(self):
        #Maximaze window
        if self.get_config_value('browser:maximize_window'):
            self._driver.maximize_window()
        else:
            #Window position
            self._driver.set_window_position(
                self.get_config_value('browser:window_x_position'),
                self.get_config_value('browser:window_y_position')
            )

            #Window size
            self._driver.set_window_size(
                self.get_config_value('browser:window_width'),
                self.get_config_value('browser:window_height')
            )

    def get_config_value(self, value):
        return self.test_instance.get_config_value(value)

    def get_ip_of_node(self, **kwargs):
        if self.browser_config.location in ['localhost', 'appium']:
            return '127.0.0.1'
        elif self.browser_config.location == 'virtualbox':
            #TODO
            raise NotImplemented()

        #EC2
        elif self.browser_config.location == 'ec2':
            exception_str = ''
            try:
                self._driver.execute_script("error")
            except WebDriverException as e:
                exception_str = str(e)

            try:
                return re.search("ip: '([^']*)", exception_str).group(1)
            except AttributeError:
                msg = "The ip address of the node could not be determined"
                self.error_log(msg)
                raise Exception(msg)

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