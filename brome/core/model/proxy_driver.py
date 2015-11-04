#! -*- coding: utf-8 -*-

from inspect import currentframe, getframeinfo
import json
import re

from sqlalchemy.exc import ProgrammingError
from selenium.webdriver.common.action_chains import ActionChains

from brome.core.model.utils import *
from brome.core.model.meta.base import Session
from brome.core.model.selector import Selector
from brome.core.model.test import Test
from brome.core.model.test_result import TestResult
from brome.core.model.proxy_element import ProxyElement
from brome.core.model.proxy_element_list import ProxyElementList

class ProxyDriver(object):
    """This class act as a proxy between the driver calls and the selenium driver

    It add functionalities or add value to existing selenium functionalities

    If the proxy driver doesn't have a particular method it automatically redirect it to the selenium native driver

    If you need to bypass the proxy driver you can by accessing the _driver directly:
        e.g.::

            pdriver._driver.find_element_by_xpath("//div")

    Attributes:
        driver (object): the native selenium driver
        test_instance (object): the test instance binded to this driver
        runner (object): the runner instance binded to this driver
    """

    def __init__(self, driver, test_instance, runner):
        self._driver = driver
        self.test_instance = test_instance
        self.runner = runner

        self.browser_config = self.test_instance._browser_config
        self.brome = self.runner.brome
        self.selector_dict = self.brome.selector_dict

        #Use when we run with the remote runner
        #We don't want to embed in this case
        self.embed_disabled = False

        self.no_javascript_error_string = 'No javascript error'
    
    def __getattr__(self, funcname):
        """Redirect to the native selenium driver when necessary
        """

        return getattr(self._driver, funcname)

    #IS
    def is_present(self, selector):
        """Check if an element is present in the dom or not

        This method won't check if the element is displayed or not
        This method won't wait until the element is visible or present
        This method won't raise any exception if the element is not present

        Returns:
            bool: True if the element is present; False otherwise
        """
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

    def is_visible(self, selector):
        """Check if an element is visible in the dom or not

        This method will check if the element is displayed or not

        This method might (according to the config highlight:element_is_visible)
        highlight the element if it is visible

        This method won't wait until the element is visible or present
        This method won't raise any exception if the element is not visible

        Returns:
            bool: True if the element is visible; False otherwise
        """

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
        """Find an element with a selector

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            wait_until_present (bool)
            wait_until_visible (bool)
            raise_exception (bool)

        Returns:
            None if no element was found
            proxy_element is an element was found

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.debug_log(u"Finding element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)
        if len(elements):
            self.debug_log(u"find (%s): Element found"%(selector))
            return elements[0]
        else:
            self.debug_log(u"find (%s): No element found"%(selector))
            return None

    def find_last(self, selector, **kwargs):
        """Return the last element found with a selector

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            wait_until_present (bool)
            wait_until_visible (bool)
            raise_exception (bool)

        Returns:
            None if no element was found
            proxy_element is an element was found

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.debug_log(u"Finding last element with selector: %s"%selector)

        elements = self.find_all(selector, **kwargs)
        if len(elements):
            self.debug_log(u"find_last (%s): element found"%selector)
            return elements[-1]
        else:
            self.debug_log(u"find_last (%s): No element found"%selector)
            return None

    def find_all(self, selector, **kwargs):
        """Return all the elements found with a selector

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            wait_until_present (bool) default configurable via proxy_driver:wait_until_present_before_find
            wait_until_visible (bool) default configurable via proxy_driver:wait_until_visible_before_find
            raise_exception (bool) default configurable via proxy_driver:raise_exception

        Returns:
            empty list if no element was found
            proxy_element_list when element are found

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

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
        """Wait until an element is clickable

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            bool True if element is clickable before the timeout, False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
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
            WebDriverWait(self._driver, timeout).until(EC.element_to_be_clickable((getattr(By, _selector.find_by), _selector.get_selector())))
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
        """Wait until an element is present

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            proxy_element: if element is present before the timeout, False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
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
        """Wait until an element is not present

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            bool: True if the element is not present before the timeout, False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
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
        """Wait until an element is visible

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            proxy_elment: if the element is visible before the timeout, False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
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
        """Wait until an element is not visible

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            bool: True if the element is not visible before the timeout, False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
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

    #FUNCTION
    def configure_resolution(self):
        #This is not supported on android
        if self.get_platform().lower() == 'android':
            return

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
            return self.runner.instances[self.browser_config.browser_id][0].get_ip()

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

    def get(self, url):
        """Navigate to a specific url

        This specific implementation inject a javascript script to intercept the javascript error
        
        Configurable with the "proxy_driver:intercept_javascript_error" config

        Args:
            url (str): the url to navigate to

        Returns:
            bool
        """
        self._driver.get(url)

        if self.get_config_value("proxy_driver:intercept_javascript_error"):
            self.init_javascript_error_interception()
        
        return True

    def inject_js_script(self, script_url):
        """inject a javascript script inside the current page

        Arguments:
            script_url: str (path)

        Returns: None
        """

        self._driver.execute_script("""
            var script = document.createElement("script");

            script.src = "%s"

            document.head.appendChild(script);
        """%script_url)

    def init_javascript_error_interception(self):
        """Inject javascript code that will gather the javascript raised
        """
        self.debug_log("Initializing javascript error interception")

        self._driver.execute_script("""
            window.jsErrors = [];
            window.onerror = function (errorMessage, url, lineNumber) {
                var message = 'Error: ' + errorMessage;
                window.jsErrors.push(message);
                return false;
            };
        """)

    def print_javascript_error(self):
        """Print to the info log the gathered javascript error

        If no error is found then nothing is printed
        """

        errors = self.get_javascript_error(return_type = 'list')
        if errors:
            self.info_log("Javascript error:")
            for error in errors:
                self.info_log(error)

    def get_javascript_error(self, return_type = 'string'):
        """Return the gathered javascript error

        Args:
            return_type: 'string' | 'list'; default: 'string'
        """

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
                    return os.linesep.join(js_errors)
                else:
                    return self.no_javascript_error_string
        else:
            self.warning_log("get_javascript_error was called but proxy_driver:intercept_javascript_error is set to False.")
            return []

    def pdb(self):
        """Start the python debugger

        Calling pdb won't do anything in a multithread context
        """
        if self.embed_disabled:
            self.warning_log("Pdb is disabled when runned from the grid runner because of the multithreading")
            return False
            
        if self.get_config_value("runner:play_sound_on_pdb"):
            say(self.get_config_value("runner:sound_on_pdb"))

        set_trace()

    def drag_and_drop(self, source_selector, destination_selector, **kwargs):
        """Drag and drop

        Args:
            source_selector: (str)
            destination_selector: (str)

        Kwargs:
            use_javascript_dnd: bool; default: config proxy_driver:use_javascript_dnd
        """
        self.info_log("Drag and drop: source (%s); destination (%s)"%(source_selector, destination_selector))

        use_javascript_dnd = kwargs.get(
            "use_javascript_dnd",
            "proxy_driver:use_javascript_dnd"
        )

        source_el = self.find(source_selector)
        destination_el = self.find(destination_selector)

        if use_javascript_dnd:
            try:
                dnd_script = """
                    function simulate(f,c,d,e){var b,a=null;for(b in eventMatchers)if(eventMatchers[b].test(c)){a=b;break}if(!a)return!1;document.createEvent?(b=document.createEvent(a),a=="HTMLEvents"?b.initEvent(c,!0,!0):b.initMouseEvent(c,!0,!0,document.defaultView,0,d,e,d,e,!1,!1,!1,!1,0,null),f.dispatchEvent(b)):(a=document.createEventObject(),a.detail=0,a.screenX=d,a.screenY=e,a.clientX=d,a.clientY=e,a.ctrlKey=!1,a.altKey=!1,a.shiftKey=!1,a.metaKey=!1,a.button=1,f.fireEvent("on"+c,a));return!0} var eventMatchers={HTMLEvents:/^(?:load|unload|abort|error|select|change|submit|reset|focus|blur|resize|scroll)$/,MouseEvents:/^(?:click|dblclick|mouse(?:down|up|over|move|out))$/};

                    var source = arguments[0],
                        destination = arguments[1];

                    simulate(source, "mousedown", 0, 0);
                    simulate(source, "mousemove", destination.offsetLeft, destination.offsetTop); 
                    simulate(source, "mouseup", destination.offsetLeft, destination.offsetTop);
                """
                self._driver.execute_script(dnd_script, source_el._element, destination_el._element)

            except Exception as e:
                self.error_log(u'drag_and_drop exception: %s'%str(e))
                raise
        else:
            try:
                ActionChains(self._driver).drag_and_drop(source_el, destination_el).perform()
            except Exception as e:
                self.error_log(u'drag_and_drop exception: %s'%str(e))
                raise

    def embed(self, title = ''):
        """Start an IPython embed

        Calling embed won't do anything in a multithread context

        The stack_depth will be found automatically
        """
        if self.embed_disabled:
            self.warning_log("Embed is disabled when runned from the grid runner because of the multithreading")
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
        """Take a screenshot
            
        Use the screenshot_name args when you want to take a screenshot for reference

        If the `runner:cache_screenshot` config is set to True then screenshot sharing all the same name will be saved only once

        The screenshot_path args is exclusively used by the proxy_driver:create_test_result function

        Args:
            screenshot_name (str) the name of the screenshot
            screenshot_path (str) the path of the screenshot
        """
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
                if self.test_instance._runner_dir:
                    screenshot_path = os.path.join(
                            self.test_instance._screenshot_dir,
                            '%s.png'%string_to_filename(screenshot_name)
                        )
                    self._driver.save_screenshot(
                        screenshot_path
                    )
                    self.debug_log(u"Screenshot taken (%s)"%screenshot_path)
        else:
            if self.test_instance._runner_dir:
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
        """Assert that the element is present in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_present (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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
        """Assert that the element is not present in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_not_present (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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
        """Assert that the element is visible in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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
                                'highlight:style_on_assertion_success'
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
        """Assert that the element is not visible in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_not_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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
        """Assert that the element's text is equal to the provided value

        Args:
            selector (str): the selector used to find the element
            value (str): the value that will be compare with the element.text value
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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
        """Assert that the element's text is not equal to the provided value

        Args:
            selector (str): the selector used to find the element
            value (str): the value that will be compare with the element.text value
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
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

    def create_test_result(self, testid, result):
        """Create a test result entry in the persistence layer

        Args:
            testid (str)
            result (bool)

        Returns:
            None
        """

        embed = True
        videocapture_path = self.test_instance._video_capture_file_relative_path
        screenshot_relative_path = ''
        extra_data = ''
        extra_data_dict = {}

        #JAVASCRIPT ERROR
        if not result:
            extra_data_dict['javascript_error'] = self.get_javascript_error()
        
        #NETWORK CAPTURE
        if self.browser_config.get('enable_proxy'):
            extra_data_dict['network_capture_path'] = os.path.join(self.test_instance._network_capture_relative_dir, string_to_filename('%s.data'%self.test_instance._name))

        if extra_data_dict:
            extra_data = json.dumps(extra_data_dict)

        session = Session()

        try:
            if not session.query(Test).filter(Test.test_id == testid).count():
                test = None
            else:
                test = session.query(Test).filter(Test.test_id == testid).one()
        except ProgrammingError:
            test = None

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
                if self.test_instance._runner_dir:
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
                if self.test_instance._runner_dir:
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
            test_instance_id = self.test_instance._test_instance_id,
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
