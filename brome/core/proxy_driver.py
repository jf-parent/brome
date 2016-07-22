from tempfile import tempdir
from inspect import currentframe
from datetime import datetime
import re
import os

from pdb import set_trace
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from brome.core.utils import (
    say,
    string_to_filename,
    DbSessionContext,
    get_timestamp
)
# from brome.core.bot_diary import BotDiary
from brome.core.settings import BROME_CONFIG
from brome.core.selector import Selector
from brome.core.proxy_element import ProxyElement
from brome.core.proxy_element_list import ProxyElementList
from brome.model.test import Test
from brome.model.testresult import Testresult
from brome.model.testqualityscreenshot import Testqualityscreenshot
from brome.model.testscreenshot import Testscreenshot


class ProxyDriver(object):
    """This class act as a proxy between the driver calls and the selenium driver

    It add functionalities or add value to existing selenium functionalities

    If the proxy driver doesn't have a particular method it
    automatically redirect it to the selenium native driver

    If you need to bypass the proxy driver you can by accessing the
    _driver directly:
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

        if BROME_CONFIG['bot_diary']['enable_bot_diary']:
            # TODO rewrite the whole thing
            # self.bot_diary = BotDiary(self)
            self.bot_diary = False
        else:
            self.bot_diary = False

        self.browser_config = self.test_instance._browser_config

        # Use when we run with the remote runner
        # We don't want to embed in this case
        self.embed_disabled = False

        self.no_javascript_error_string = 'No javascript error'

    def __getattr__(self, funcname):
        """Redirect to the native selenium driver when necessary
        """

        return getattr(self._driver, funcname)

    # IS
    def is_present(self, selector):
        """Check if an element is present in the dom or not

        This method won't check if the element is displayed or not
        This method won't wait until the element is visible or present
        This method won't raise any exception if the element is not present

        Returns:
            bool: True if the element is present; False otherwise
        """
        self.debug_log("Is present (%s)" % selector)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_present=False,
            wait_until_visible=False
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

        This method might (according
        to the config highlight:element_is_visible)
        highlight the element if it is visible

        This method won't wait until the element is visible or present
        This method won't raise any exception if the element is not visible

        Returns:
            bool: True if the element is visible; False otherwise
        """

        self.debug_log("Is visible (%s)" % selector)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_present=False,
            wait_until_visible=False
        )

        if element:
            if element.is_displayed(raise_exception=False):

                element.highlight(
                    style=BROME_CONFIG['highlight']['element_is_visible']
                )

                self.debug_log("is visible (%s): True" % selector)

                return True

        self.debug_log("is visible (%s): False" % selector)

        return False

    # FIND
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
            this function might raise an exception
                depending on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.debug_log("Finding element with selector: %s" % selector)

        elements = self.find_all(selector, **kwargs)
        if len(elements):
            self.debug_log("find (%s): Element found" % (selector))
            return elements[0]
        else:
            self.debug_log("find (%s): No element found" % (selector))
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
            this function might raise an exception depending
                on the raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.debug_log("Finding last element with selector: %s" % selector)

        elements = self.find_all(selector, **kwargs)
        if len(elements):
            self.debug_log("find_last (%s): element found" % selector)
            return elements[-1]
        else:
            self.debug_log("find_last (%s): No element found" % selector)
            return None

    def find_all(self, selector, **kwargs):
        """Return all the elements found with a selector

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            wait_until_present (bool) default configurable via
                proxy_driver:wait_until_present_before_find
            wait_until_visible (bool) default configurable via
                proxy_driver:wait_until_visible_before_find
            raise_exception (bool) default configurable via
                proxy_driver:raise_exception

        Returns:
            empty list if no element was found
            proxy_element_list when element are found

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.debug_log("Finding elements with selector: %s" % selector)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        wait_until_present = kwargs.get(
            'wait_until_present',
            BROME_CONFIG['proxy_driver']['wait_until_present_before_find']
        )

        self.debug_log(
            "effective wait_until_present: %s" % wait_until_present
        )

        wait_until_visible = kwargs.get(
            'wait_until_visible',
            BROME_CONFIG['proxy_driver']['wait_until_visible_before_find']
        )
        self.debug_log(
            "effective wait_until_visible: %s" % wait_until_visible
        )

        _selector = Selector(self, selector)

        found = False
        if wait_until_visible:
            # we don't raise exception here otherwise none visible
            # element will always raise exception
            # TODO find a good way to make it configurable
            found = self.wait_until_visible(selector, raise_exception=False)

        if wait_until_present and not found:
            found = self.wait_until_present(
                selector,
                raise_exception=raise_exception
            )
            if not found:
                self.debug_log("find_all (%s): No element found" % _selector)
                return []

        try:
            elements = getattr(
                self._driver,
                _selector.find_function
            )(_selector.get_selector())
        except exceptions.NoSuchElementException:
            self.debug_log("find_all (%s): No element found" % _selector)
            self.print_javascript_error()
            if raise_exception:
                raise exceptions.NoSuchElementException(_selector)
            else:
                return []

        if type(elements) == list:
            if len(elements):
                self.debug_log("find_all (%s): Element found" % _selector)
                return ProxyElementList(elements, _selector, self)
            else:
                msg = "find_all (%s): No element found" % _selector
                self.debug_log(msg)
                self.print_javascript_error()
                if raise_exception:
                    raise exceptions.NoSuchElementException(msg)
                else:
                    return []
        else:
            self.debug_log("find_all (%s): Element found" % _selector)
            return [ProxyElement(elements, _selector, self)]

    # WAIT
    def wait_until_clickable(self, selector, **kwargs):
        """Wait until an element is clickable

        Args:
            selector (str): the selector used to find the element

        Kwargs:
            timeout (int) second before a timeout exception is raise
            raise_exception (bool) raise an exception or return a bool

        Returns:
            bool True if element is clickable before the timeout,
                False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
        self.info_log("Waiting until clickable (%s)" % selector)

        timeout = kwargs.get(
            'timeout',
            BROME_CONFIG['proxy_driver']['default_timeout']
        )
        self.debug_log("effective timeout: %s" % timeout)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        _selector = Selector(self, selector)

        try:
            WebDriverWait(
                self._driver, timeout
            ).until(
                EC.element_to_be_clickable(
                    (getattr(By, _selector.find_by), _selector.get_selector()))
            )
            self.debug_log(
                "wait_until_clickable (%s): element is clickable" % _selector
            )
            return True
        except exceptions.TimeoutException:
            msg = "wait_until_clickable: element (%s) is still not clickable" % _selector  # noqa
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                if self.bot_diary:
                    self.bot_diary.add_auto_entry(
                        "I waited for the clickability of",
                        target=_selector.get_human_readable()
                    )
                raise exceptions.TimeoutException(msg)
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
            proxy_element: if element is present before the timeout,
                False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
        self.info_log(
            "Waiting until present (%s)" % selector
        )

        timeout = kwargs.get(
            'timeout',
            BROME_CONFIG['proxy_driver']['default_timeout']
        )
        self.debug_log("effective timeout: %s" % timeout)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        _selector = Selector(self, selector)
        try:
            el = WebDriverWait(
                self._driver, timeout
            ).until(
                EC.presence_of_element_located(
                    (getattr(By, _selector.find_by), _selector.get_selector())
                )
            )
            self.debug_log(
                "wait_until_present (%s): element is present" % _selector
            )
            return ProxyElement(el, _selector, self)
        except exceptions.TimeoutException:
            msg = "wait_until_present (%s): element is still not present" % _selector  # noqa
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                if self.bot_diary:
                    self.bot_diary.add_auto_entry(
                        "I waited for the presence of",
                        target=_selector.get_human_readable()
                    )
                raise exceptions.TimeoutException(msg)
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
            bool: True if the element is not present before the timeout,
                False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
        self.info_log("Waiting until not present (%s)" % selector)

        timeout = kwargs.get(
            'timeout',
            BROME_CONFIG['proxy_driver']['default_timeout']
        )
        self.debug_log("effective timeout: %s" % timeout)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        _selector = Selector(self, selector)
        try:
            WebDriverWait(
                self._driver, timeout
            ).until(
                EC.invisibility_of_element_located(
                    (getattr(By, _selector.find_by), _selector.get_selector())
                )
            )
            self.debug_log(
                "wait_until_not_present (%s): element is not present" % _selector  # noqa
            )
            return True
        except exceptions.TimeoutException:
            msg = "wait_until_not_present (%s): element is still present" % _selector  # noqa
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                if self.bot_diary:
                    self.bot_diary.add_auto_entry(
                        "I waited for the absence of",
                        target=_selector.get_human_readable()
                    )
                raise exceptions.TimeoutException(msg)
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
            proxy_elment: if the element is visible before the timeout,
                False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """

        self.info_log("Waiting until visible (%s)" % selector)

        timeout = kwargs.get(
            'timeout',
            BROME_CONFIG['proxy_driver']['default_timeout']
        )
        self.debug_log("effective timeout: %s" % timeout)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        _selector = Selector(self, selector)
        try:
            el = WebDriverWait(
                self._driver, timeout
            ).until(
                EC.visibility_of_element_located(
                    (getattr(By, _selector.find_by), _selector.get_selector())
                )
            )
            self.debug_log(
                "wait_until_visible (%s): element is visible" % _selector
            )
            return ProxyElement(el, _selector, self)
        except exceptions.TimeoutException:
            msg = "wait_until_visible (%s): element is still not visible" % _selector  # noqa
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                if self.bot_diary:
                    self.bot_diary.add_auto_entry(
                        "I waited for the visibility of", target=_selector.get_human_readable()  # noqa
                    )
                raise exceptions.TimeoutException(msg)
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
            bool: True if the element is not visible before the timeout,
                False otherwise (raise_exception = False)

        Raises:
            this function might raise an exception depending on the
                raise_exception kwargs
            or
            the config proxy_driver:raise_exception
        """
        self.info_log("Waiting until not visible (%s)" % selector)

        timeout = kwargs.get(
            'timeout',
            BROME_CONFIG['proxy_driver']['default_timeout']
        )
        self.debug_log("effective timeout: %s" % timeout)

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        self.debug_log("effective raise_exception: %s" % raise_exception)

        _selector = Selector(self, selector)
        try:
            WebDriverWait(
                self._driver, timeout
            ).until(
                EC.invisibility_of_element_located(
                    (getattr(By, _selector.find_by), _selector.get_selector())
                )
            )
            self.debug_log(
                "wait_until_not_visible (%s): element is not visible" % _selector  # noqa
            )
            return True
        except exceptions.TimeoutException:
            msg = "wait_until_not_visible (%s): element is still visible" % _selector  # noqa
            self.debug_log(msg)
            self.print_javascript_error()
            if raise_exception:
                if self.bot_diary:
                    self.bot_diary.add_auto_entry(
                        "I waited for the invisibility of",
                        target=_selector.get_human_readable()
                    )
                raise exceptions.TimeoutException(msg)
            else:
                return False

    # FUNCTION
    def configure_resolution(self):
        # This is not supported on android
        if self.get_platform().lower() == 'android':
            return

        # Maximaze window
        if BROME_CONFIG['browser']['maximize_window']:
            self._driver.maximize_window()
        elif BROME_CONFIG['browser'].get('dont_resize', False):
            return
        else:
            # Window position
            self._driver.set_window_position(
                BROME_CONFIG['browser']['window_x_position'],
                BROME_CONFIG['browser']['window_y_position']
            )

            # Window size
            self._driver.set_window_size(
                BROME_CONFIG['browser']['window_width'],
                BROME_CONFIG['browser']['window_height']
            )

    def get_ip_of_node(self, **kwargs):
        if self.browser_config.location in ['localhost', 'appium']:
            return '127.0.0.1'

        elif self.browser_config.location == 'virtualbox':
            return self.runner.instances[self.browser_config.browser_id][0].get_ip()  # noqa

        # EC2
        elif self.browser_config.location == 'ec2':
            if self.browser_config.get('browserName') == 'dummy':
                return '127.0.0.1'
            else:
                exception_str = ''
                try:
                    self._driver.execute_script("error")
                except exceptions.WebDriverException as e:
                    exception_str = str(e)

                try:
                    return re.search("ip: '([^']*)", exception_str).group(1)
                except AttributeError:
                    msg = "The ip address of the node could not be determined"
                    self.error_log(msg)
                    raise Exception(msg)

    def get_id(
                self,
                join_char='-',
                browser_version_join_char='_',
                platform_join_char='_'):

        return join_char.join([
                    self.get_browser_name(),
                    self.get_browser_version(
                        join_char=browser_version_join_char
                    ),
                    self.get_platform(join_char=platform_join_char)
                ])

    def get_browser_name(self):
        if self.browser_config.get('fakeIdentity'):
            return self.browser_config.get('fakeIdentity').title()
        else:
            return self._driver.capabilities['browserName'].title()

    def get_browser_version(self, join_char='_'):
        return self._driver.capabilities['version'].replace('.', join_char)

    def get_platform(self, join_char='_'):
        return self._driver.capabilities['platform'].replace('.', join_char)

    def get(self, url):
        """Navigate to a specific url

        This specific implementation inject a javascript
            script to intercept the javascript error

        Configurable with the "proxy_driver:intercept_javascript_error" config

        Args:
            url (str): the url to navigate to

        Returns:
            bool
        """

        self._driver.get(url)

        if self.bot_diary:
            self.bot_diary.add_auto_entry(
                "I went on",
                target=url,
                take_screenshot=True
            )

        if BROME_CONFIG['proxy_driver']['intercept_javascript_error']:
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
        """ % script_url)

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

        errors = self.get_javascript_error(return_type='list')
        if errors:
            self.info_log("Javascript error:")
            for error in errors:
                self.info_log(error)

    def get_javascript_error(self, return_type='string'):
        """Return the gathered javascript error

        Args:
            return_type: 'string' | 'list'; default: 'string'
        """

        if BROME_CONFIG['proxy_driver']['intercept_javascript_error']:
            js_errors = self._driver.execute_script(
                'return window.jsErrors; window.jsErrors = [];'
            )

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
            return []

    def pdb(self):
        """Start the python debugger

        Calling pdb won't do anything in a multithread context
        """
        if self.embed_disabled:
            self.warning_log("Pdb is disabled when runned from the grid runner because of the multithreading")  # noqa
            return False

        if BROME_CONFIG['runner']['play_sound_on_pdb']:
            say(BROME_CONFIG['runner']['sound_on_pdb'])

        set_trace()

    def drag_and_drop(self, source_selector, destination_selector, **kwargs):
        """Drag and drop

        Args:
            source_selector: (str)
            destination_selector: (str)

        Kwargs:
            use_javascript_dnd: bool; default:
                config proxy_driver:use_javascript_dnd
        """
        self.info_log(
            "Drag and drop: source (%s); destination (%s)" %
            (source_selector, destination_selector)
        )

        use_javascript_dnd = kwargs.get(
            "use_javascript_dnd",
            "proxy_driver:use_javascript_dnd"
        )

        source_el = self.find(source_selector)
        destination_el = self.find(destination_selector)

        if use_javascript_dnd:
            try:
                dnd_script = [
                    "function simulate(f,c,d,e){var b,a=null;for(b in eventMatchers)if(eventMatchers[b].test(c)){a=b;break}if(!a)return!1;document.createEvent?(b=document.createEvent(a),a=='HTMLEvents'?b.initEvent(c,!0,!0):b.initMouseEvent(c,!0,!0,document.defaultView,0,d,e,d,e,!1,!1,!1,!1,0,null),f.dispatchEvent(b)):(a=document.createEventObject(),a.detail=0,a.screenX=d,a.screenY=e,a.clientX=d,a.clientY=e,a.ctrlKey=!1,a.altKey=!1,a.shiftKey=!1,a.metaKey=!1,a.button=1,f.fireEvent('on'+c,a));return!0} var eventMatchers={HTMLEvents:/^(?:load|unload|abort|error|select|change|submit|reset|focus|blur|resize|scroll)$/,MouseEvents:/^(?:click|dblclick|mouse(?:down|up|over|move|out))$/};",  # noqa
                    "var source = arguments[0],destination = arguments[1];",
                    "simulate(source, 'mousedown', 0, 0);",
                    "simulate(source, 'mousemove', destination.offsetLeft, destination.offsetTop);",  # noqa
                    "simulate(source, 'mouseup', destination.offsetLeft, destination.offsetTop);"  # noqa
                ]
                self._driver.execute_script(
                    '\n'.join(dnd_script),
                    source_el._element,
                    destination_el._element
                )

            except Exception as e:
                self.error_log(u'drag_and_drop exception: %s' % str(e))
                raise
        else:
            try:
                ActionChains(self._driver).drag_and_drop(
                    source_el,
                    destination_el
                ).perform()
            except Exception as e:
                self.error_log(u'drag_and_drop exception: %s' % str(e))
                raise

    def embed(self, title=''):
        """Start an IPython embed

        Calling embed won't do anything in a multithread context

        The stack_depth will be found automatically
        """
        if self.embed_disabled:
            self.warning_log("Embed is disabled when runned from the grid runner because of the multithreading")  # noqa
            return False

        from IPython.terminal.embed import InteractiveShellEmbed

        if BROME_CONFIG['runner']['play_sound_on_ipython_embed']:
            say(BROME_CONFIG['runner']['sound_on_ipython_embed'])

        ipshell = InteractiveShellEmbed(banner1=title)

        frame = currentframe()
        stack_depth = 1
        for i in range(5):
            frame = frame.f_back
            stack_depth += 1
            if frame.f_code.co_filename not in __file__:
                break

        msg = 'Stopped at %s and line %s;' % \
            (frame.f_code.co_filename, frame.f_lineno)

        ipshell(msg, stack_depth=stack_depth)

    def take_node_screenshot(self, element, screenshot_path):
        from PIL import Image
        """Take a screenshot of a node

        Args:
            element (object): the proxy_element
            screenshot_path (str): the path where the screenshot will be saved
        """

        temp_path = os.path.join(tempdir, screenshot_path)

        el_x = int(element.location['x'])
        el_y = int(element.location['y'])
        el_height = int(element.size['height'])
        el_width = int(element.size['width'])

        if el_height == 0 or el_width == 0:
            self.debug_log("take_node_screenshot cannot be taken because element width or height equal zero")  # noqa
            return False

        bounding_box = (
            el_x,
            el_y,
            (el_x + el_width),
            (el_y + el_height)
        )

        self._driver.save_screenshot(temp_path)

        base_image = Image.open(temp_path)

        cropped_image = base_image.crop(bounding_box)

        base_image = base_image.resize(cropped_image.size)

        base_image.paste(cropped_image, (0, 0))

        base_image.save(screenshot_path)

        """
        except Exception as e:
            tb = traceback.format_exc()
            print unicode(tb)
            embed()
        """

    def take_screenshot(self, screenshot_name=None, screenshot_path=None):
        """Take a screenshot

        Use the screenshot_name args when you want to take a
            screenshot for reference

        If the `runner:cache_screenshot` config is set to True then
            screenshot sharing all the same name will be saved only once

        The screenshot_path args is exclusively used by the
            proxy_driver:create_test_result function

        Args:
            screenshot_name (str) the name of the screenshot
            screenshot_path (str) the path of the screenshot
        """
        self.info_log("Taking a screenshot...")

        save_to_db = False
        if screenshot_path:
            self._driver.save_screenshot(screenshot_path)
            self.debug_log("Screenshot taken (%s)" % screenshot_path)

        elif screenshot_name:
            take_screenshot = True
            if hasattr(self.runner, "screenshot_cache"):
                if self.runner.screenshot_cache.get(screenshot_name):
                    self.debug_log(
                        "screenshot(%s) found in cache" % screenshot_name
                    )
                    take_screenshot = False

            if take_screenshot:
                if self.test_instance._runner_dir:
                    screenshot_name = '%s.png' % \
                        string_to_filename(screenshot_name)

                    relative_path = os.path.join(
                            self.test_instance._screenshot_relative_dir,
                            screenshot_name
                    )

                    full_path = os.path.join(
                            self.test_instance._screenshot_dir,
                            screenshot_name
                    )

                    self._driver.save_screenshot(
                        full_path
                    )
                    self.debug_log("Screenshot taken (%s)" % full_path)
                    save_to_db = True
        else:
            if self.test_instance._runner_dir:
                screenshot_name = '%s.png' % get_timestamp()

                relative_path = os.path.join(
                        self.test_instance._screenshot_relative_dir,
                        screenshot_name
                )

                full_path = os.path.join(
                        self.test_instance._screenshot_dir,
                        screenshot_name
                )

                self._driver.save_screenshot(
                    full_path
                )
                self.debug_log("Screenshot taken (%s)" % full_path)
                save_to_db = True

        if save_to_db:
            with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                screenshot = Testscreenshot()
                screenshot.browser_capabilities = self.capabilities
                screenshot.browser_id = self.get_id()
                # TODO support s3
                screenshot.location = 'local_file_system'
                screenshot.root_path = self.test_instance._runner.root_test_result_dir  # noqa
                screenshot.file_path = relative_path
                screenshot.extra_data = {}
                screenshot.title = screenshot_name
                screenshot.test_instance_id = self.test_instance._test_instance_id  # noqa
                screenshot.test_batch_id = self.test_instance._test_batch_id  # noqa

                session.save(screenshot, safe=True)

    def take_quality_screenshot(self, screenshot_name):
        """Take a quality screenshot

        Use the screenshot_name args when you want to take a
            screenshot for reference

        Args:
            screenshot_name (str) the name of the screenshot
        """
        self.info_log("Taking a quality screenshot...")

        if self.test_instance._runner_dir:
            screenshot_name = '%s.png' % string_to_filename(screenshot_name)
            relative_path = os.path.join(
                    self.test_instance._quality_screenshot_relative_dir,
                    screenshot_name
                )

            full_path = os.path.join(
                    self.test_instance._quality_screenshot_dir,
                    screenshot_name
                )
            self._driver.save_screenshot(
                full_path
            )

            with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                quality_screenshot = Testqualityscreenshot()
                quality_screenshot.timestamp = datetime.now()
                quality_screenshot.browser_capabilities = self.capabilities
                quality_screenshot.browser_id = self.get_id()
                quality_screenshot.file_path = relative_path
                # TODO support s3
                quality_screenshot.location = 'local_file_system'
                quality_screenshot.root_path = self.test_instance._runner.root_test_result_dir  # noqa
                quality_screenshot.extra_data = {}
                quality_screenshot.title = screenshot_name
                quality_screenshot.test_instance_id = self.test_instance._test_instance_id  # noqa
                quality_screenshot.test_batch_id = self.test_instance._test_batch_id  # noqa

                session.save(quality_screenshot, safe=True)

            self.debug_log("Quality screenshot taken (%s)" % full_path)

    # ASSERT
    def assert_present(self, selector, testid=None, **kwargs):
        """Assert that the element is present in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_present (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
        self.info_log(
            "Assert present selector(%s) testid(%s)" % (selector, testid)
        )

        wait_until_present = kwargs.get(
            'wait_until_present',
            BROME_CONFIG['proxy_driver']['wait_until_present_before_assert_present']  # noqa
        )
        self.debug_log(
            "effective wait_until_present: %s" % wait_until_present
        )

        if wait_until_present:
            element = self.wait_until_present(selector, raise_exception=False)
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

    def assert_not_present(self, selector, testid=None, **kwargs):
        """Assert that the element is not present in the dom

        Args:
            selector (str): the selector used to find the element
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_not_present (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
        self.info_log(
            "Assert not present selector(%s) testid(%s)" %
            (selector, testid)
        )

        wait_until_not_present = kwargs.get(
            'wait_until_not_present',
            BROME_CONFIG['proxy_driver']['wait_until_not_present_before_assert_not_present']  # noqa
        )
        self.debug_log(
            "effective wait_until_not_present: %s" % wait_until_not_present
        )

        if wait_until_not_present:
            ret = self.wait_until_not_present(selector, raise_exception=False)
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

    def assert_visible(self, selector, testid=None, **kwargs):
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
        self.info_log(
            "Assert visible selector(%s) testid(%s)" % (selector, testid)
        )

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_on_assertion_success']
        )
        self.debug_log("effective highlight: %s" % highlight)

        wait_until_visible = kwargs.get(
            'wait_until_visible',
            BROME_CONFIG['proxy_driver']['wait_until_visible_before_assert_visible']  # noqa
        )
        self.debug_log("effective wait_until_visible: %s" % wait_until_visible)

        if wait_until_visible:
            self.wait_until_visible(selector, raise_exception=False)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_visible=False,
            wait_until_present=False
        )
        if element and element.is_displayed(raise_exception=False):
            if highlight:
                element.highlight(
                    style=BROME_CONFIG['highlight']['style_on_assertion_success']  # noqa
                )
            if testid is not None:
                self.create_test_result(testid, True)

            return True
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_not_visible(self, selector, testid=None, **kwargs):
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
        self.info_log(
            "Assert not visible selector(%s) testid(%s)" % (selector, testid)
        )

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_on_assertion_failure']
        )
        self.debug_log("effective highlight: %s" % highlight)

        wait_until_not_visible = kwargs.get(
            'wait_until_not_visible',
            BROME_CONFIG['proxy_driver']['wait_until_not_visible_before_assert_not_visible']  # noqa
        )
        self.debug_log(
            "effective wait_until_not_visible: %s" % wait_until_not_visible
        )

        if wait_until_not_visible:
            self.wait_until_not_visible(selector, raise_exception=False)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_visible=False,
            wait_until_present=False
        )
        if element and element.is_displayed(raise_exception=False):
            data = self.execute_script(
                "return arguments[0].getBoundingClientRect();",
                element._element
            )

            if highlight:
                element.highlight(
                    style=BROME_CONFIG['highlight']['style_on_assertion_failure']  # noqa
                )
            if testid is not None:
                self.create_test_result(testid, False, extra_data={
                    'bounding_client_rect': data,
                    'video_x_offset': self.browser_config.get('video_x_offset', 0),  # noqa
                    'video_y_offset': self.browser_config.get('video_y_offset', 0)  # noqa
                })

            return False
        else:
            if testid is not None:
                self.create_test_result(testid, True)

            return True

    def assert_text_equal(self, selector, value, testid=None, **kwargs):
        """Assert that the element's text is equal to the provided value

        Args:
            selector (str): the selector used to find the element
            value (str): the value that will be compare
                with the element.text value
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
        self.info_log(
            "Assert text equal selector(%s) testid(%s)" % (selector, testid)
        )

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_on_assertion_success']
        )
        self.debug_log("effective highlight: %s" % highlight)

        wait_until_visible = kwargs.get(
            'wait_until_visible',
            BROME_CONFIG['proxy_driver:wait_until_visible_before_assert_visible']  # noqa
        )
        self.debug_log("effective wait_until_visible: %s" % wait_until_visible)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_visible=wait_until_visible
        )
        if element:
            if element.text == value:
                if highlight:
                    element.highlight(
                        BROME_CONFIG['highlight']['style_on_assertion_success']
                    )
                if testid is not None:
                    self.create_test_result(testid, True)

                return True
            else:
                if highlight:
                    element.highlight(
                        style=BROME_CONFIG['highlight']['style_on_assertion_failure']  # noqa
                    )
                if testid is not None:
                    self.create_test_result(testid, False)

                return False
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def assert_text_not_equal(self, selector, value, testid=None, **kwargs):
        """Assert that the element's text is not equal to the provided value

        Args:
            selector (str): the selector used to find the element
            value (str): the value that will be compare with
                the element.text value
            test_id (str): the test_id or a str

        Kwargs:
            wait_until_visible (bool)
            highlight (bool)

        Returns:
            bool: True is the assertion succeed; False otherwise.
        """
        self.info_log(
            "Assert text not equal selector(%s) testid(%s)" %
            (selector, testid)
        )

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_on_assertion_success']
        )
        self.debug_log("effective highlight: %s" % highlight)

        wait_until_visible = kwargs.get(
            'wait_until_visible',
            BROME_CONFIG['proxy_driver']['wait_until_visible_before_assert_visible']  # noqa
        )
        self.debug_log("effective wait_until_visible: %s" % wait_until_visible)

        element = self.find(
            selector,
            raise_exception=False,
            wait_until_visible=wait_until_visible
        )
        if element:
            if element.text != value:
                if highlight:
                    element.highlight(
                        style=BROME_CONFIG['highlight']['style_on_assertion_success']  # noqa
                    )
                if testid is not None:
                    self.create_test_result(testid, True)

                return True
            else:
                if highlight:
                    element.highlight(
                        BROME_CONFIG['highlight']['style_on_assertion_failure']  # noqa
                    )
                if testid is not None:
                    self.create_test_result(testid, False)

                return False
        else:
            if testid is not None:
                self.create_test_result(testid, False)

            return False

    def create_test_result(self, testid, result, **kwargs):
        """Create a test result entry in the persistence layer

        Args:
            testid (str)
            result (bool)

        Keyword Args:
            extra_data (dict): the extra data that will be
                saved with the test result

        Returns:
            None
        """

        embed = True
        videocapture_path = self.test_instance._video_capture_file_relative_path  # noqa
        screenshot_relative_path = ''
        extra_data = {}

        # JAVASCRIPT ERROR
        if not result:
            extra_data['javascript_error'] = self.get_javascript_error()

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            if testid in BROME_CONFIG['test_dict']:
                test = session.query(Test).filter(Test.test_id == testid).one()
                test_config = BROME_CONFIG['test_dict'][testid]
                if type(test_config) == dict:
                    if 'embed' in test_config:
                        embed = test_config['embed']
                        test_name = test_config['name']
                else:
                    test_name = test_config

                embed_title = '[%s] %s' % (testid, test_name)
            else:
                test = None
                test_name = testid
                embed_title = test_name

            if result:
                # SCREENSHOT
                if BROME_CONFIG['proxy_driver']['take_screenshot_on_assertion_success']:  # noqa
                    if self.test_instance._runner_dir:
                        screenshot_name = 'succeed_%s_%s_%s.png' % (
                            string_to_filename(testid),
                            get_timestamp(),
                            self.get_id(join_char='_')
                        )
                        screenshot_path = os.path.join(
                            self.test_instance._assertion_screenshot_dir,
                            screenshot_name
                        )
                        screenshot_relative_path = os.path.join(
                            self.test_instance._assertion_screenshot_relative_dir,  # noqa
                            screenshot_name
                        )
                        self.take_screenshot(screenshot_path=screenshot_path)

                # SOUND NOTIFICATION
                if BROME_CONFIG['runner']['play_sound_on_assertion_success']:  # noqa
                    say(
                        BROME_CONFIG['runner']['sound_on_assertion_success']
                        .format(testid=testid)
                    )

                # EMBED
                if BROME_CONFIG['runner']['embed_on_assertion_success'] and embed:  # noqa
                    self.embed(title=embed_title)
            else:
                # SCREENSHOT
                if BROME_CONFIG['proxy_driver']['take_screenshot_on_assertion_failure']:  # noqa
                    if self.test_instance._runner_dir:
                        screenshot_name = 'failed_%s_%s_%s.png' % (
                            string_to_filename(testid),
                            get_timestamp(),
                            self.get_id(join_char='_')
                        )
                        screenshot_path = os.path.join(
                            self.test_instance._assertion_screenshot_dir,
                            screenshot_name
                        )
                        screenshot_relative_path = os.path.join(
                            self.test_instance._assertion_screenshot_relative_dir,  # noqa
                            screenshot_name
                        )
                        self.take_screenshot(screenshot_path=screenshot_path)

                # SOUND NOTIFICATION
                if BROME_CONFIG['runner']['play_sound_on_assertion_failure']:  # noqa
                    say(
                        BROME_CONFIG['runner']['sound_on_assertion_failure']
                        .format(testid=testid)
                    )

                # EMBED
                if BROME_CONFIG['runner']['embed_on_assertion_failure'] and embed:  # noqa
                    self.embed(title=embed_title)

            test_result = Testresult()
            test_result.result = result
            test_result.timestamp = datetime.now()
            test_result.browser_capabilities = self.capabilities
            test_result.browser_id = self.get_id()
            test_result.root_path = self.test_instance._runner.root_test_result_dir  # noqa
            test_result.screenshot_path = screenshot_relative_path
            test_result.video_capture_path = videocapture_path
            test_result.extra_data = extra_data
            test_result.title = test_name
            test_result.test_id = test.get_uid()
            test_result.test_instance_id = self.test_instance._test_instance_id
            test_result.test_batch_id = self.runner.test_batch_id

            session.save(test_result, safe=True)

    # LOG
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
