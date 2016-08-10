import traceback
from time import sleep

from selenium.webdriver.common.touch_actions import TouchActions
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains

from brome.core.settings import BROME_CONFIG


class ProxyElement(object):

    def __init__(self, element, selector, pdriver):
        self._element = element
        self.selector = selector
        self.pdriver = pdriver

    def __getattr__(self, funcname):
        return getattr(self._element, funcname)

    def error_log(self, msg):
        self.pdriver.error_log("[%s] %s" % (self.__repr__(), msg))

    def debug_log(self, msg):
        self.pdriver.debug_log("[%s] %s" % (self.__repr__(), msg))

    def __repr__(self):
        msg = ["WebElement (selector: '%s')" % self.selector.get_selector()]

        try:
            if self._element.get_attribute('id'):
                msg.append("(id: '%s')" % self._element.get_attribute('id'))

            if self._element.get_attribute('name'):
                msg.append(
                    "(name: '%s')" % self._element.get_attribute('name')
                )

            if self._element.get_attribute('class'):
                msg.append(
                    "(class: '%s')" % self._element.get_attribute('class')
                )

        except Exception as e:
            self.pdriver.debug_log("exception in __repr__: %s" % e)

        return ' '.join(msg)

    def is_displayed(self, **kwargs):
        self.debug_log("Is displayed")

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        retry = kwargs.get('retry', True)

        try:
            is_displayed = self._element.is_displayed()
            self.debug_log("is displayed")
            return is_displayed
        except exceptions.StaleElementReferenceException:
            if retry:
                # NOTE this is an imperfect solution since we can
                # have found the element with find_last
                # TODO find a better way to handle this edge case
                self.debug_log("StaleElementReferenceException; retrying...")
                self._element = self.pdriver.find(
                    self.selector._selector,
                    raise_exception=False
                )
                if self._element:
                    return self.is_displayed(retry=False)
                else:
                    return False
            else:
                if raise_exception:
                    raise
                else:
                    return False

    def click(self, **kwargs):
        self.debug_log("Clicking on element")

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_when_element_is_clicked']
        )
        wait_until_clickable = kwargs.get(
            'wait_until_clickable',
            BROME_CONFIG['proxy_element']['wait_until_clickable']
        )

        if wait_until_clickable:
            # TODO manage the raise exception better
            self.pdriver.wait_until_clickable(
                self.selector._selector,
                raise_exception=True
            )

        if highlight:
            self.highlight(
                style=BROME_CONFIG['highlight']['style_when_element_is_clicked']  # noqa
            )

        def _click():
            if BROME_CONFIG['proxy_element']['use_touch_instead_of_click']:
                touch_action = TouchActions(self.pdriver._driver)
                touch_action.tap(self._element).perform()
            else:
                self._element.click()

        if self.pdriver.bot_diary:
            self.pdriver.bot_diary.add_auto_entry(
                "I clicked on",
                selector=self.selector._selector
            )

        try:
            _click()
        except (
                    exceptions.InvalidElementStateException,
                    exceptions.WebDriverException
                ) as e:
            self.debug_log("click exception: %s" % e)
            sleep(2)
            self.scroll_into_view()
            _click()
        except exceptions.StaleElementReferenceException as e:
            self.debug_log(
                "click exception StaleElementReferenceException: %s" % e
            )
            sleep(2)
            self._element = self.pdriver.find(self.selector._selector)
            _click()

        return True

    def double_click(self, **kwargs):
        self.debug_log("Double clicking on element")

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_when_element_is_clicked']
        )
        wait_until_clickable = kwargs.get(
            'wait_until_clickable',
            BROME_CONFIG['proxy_element']['wait_until_clickable']
        )

        if wait_until_clickable:
            # TODO manage the raise exception better
            self.pdriver.wait_until_clickable(
                self.selector._selector,
                raise_exception=True
            )

        if highlight:
            self.highlight(
                style=BROME_CONFIG['highlight']['style_when_element_is_clicked']  # noqa
            )

        def _double_click():
            if BROME_CONFIG['proxy_element']['use_touch_instead_of_click']:
                touch_action = TouchActions(self.pdriver._driver)
                touch_action.double_tap(self._element).perform()
            else:
                ActionChains(self.pdriver)\
                    .double_click(self._element).perform()

        if self.pdriver.bot_diary:
            self.pdriver.bot_diary.add_auto_entry(
                "I double clicked on",
                selector=self.selector._selector
            )

        try:
            _double_click()
        except (
                    exceptions.InvalidElementStateException,
                    exceptions.WebDriverException
                ) as e:
            self.debug_log("click exception: %s" % e)
            sleep(2)
            self.scroll_into_view()
            _double_click()
        except exceptions.StaleElementReferenceException as e:
            self.debug_log(
                "click exception StaleElementReferenceException: %s" % e
            )
            sleep(2)
            self._element = self.pdriver.find(self.selector._selector)
            _double_click()

        return True

    def send_keys(self, value, **kwargs):
        self.debug_log("Sending keys")

        highlight = kwargs.get(
            'highlight',
            BROME_CONFIG['highlight']['highlight_when_element_receive_keys']  # noqa
        )
        wait_until_clickable = kwargs.get(
            'wait_until_clickable',
            BROME_CONFIG['proxy_element']['wait_until_clickable']
        )

        if wait_until_clickable:
            # TODO manage the raise exception better
            self.pdriver.wait_until_clickable(
                self.selector._selector,
                raise_exception=True
            )

        if highlight:
            self.highlight(
                style=BROME_CONFIG['highlight']['style_when_element_receive_keys']  # noqa
            )

        clear = kwargs.get('clear', False)

        if clear:
            self.clear()

        if self.pdriver.bot_diary:
            self.pdriver.bot_diary.add_auto_entry(
                "I typed '%s' in" % value,
                selector=self.selector._selector
            )

        try:
            self._element.send_keys(value)
        except exceptions.StaleElementReferenceException as e:
            self.debug_log(
                "send_keys exception StaleElementReferenceException: %s" % e
            )
            sleep(2)
            self._element = self.pdriver.find(self.selector._selector)
            self._element.send_keys(value)
        except (
                exceptions.InvalidElementStateException,
                exceptions.WebDriverException
                ) as e:
            self.debug_log("send_keys exception: %s" % e)
            sleep(2)
            self._element.send_keys(value)

        return True

    def clear(self):
        self.debug_log("Clearing element")

        try:
            self._element.clear()
        except (
                exceptions.InvalidElementStateException,
                exceptions.WebDriverException
                ) as e:
            self.debug_log("send_keys exception: %s" % e)
            sleep(2)
            self._element.clear()
        except exceptions.StaleElementReferenceException as e:
            self.debug_log(
                "send_keys exception StaleElementReferenceException: %s" % e
            )
            sleep(2)
            self._element = self.pdriver.find(self.selector._selector)
            self._element.clear()

        return True

    def highlight(self, **kwargs):
        """
            kwargs:
                style: css
                highlight_time: int; default: .3
        """

        self.debug_log("Highlighting element")

        style = kwargs.get('style')
        highlight_time = kwargs.get('highlight_time', .3)

        driver = self._element._parent

        try:
            original_style = self._element.get_attribute('style')

            driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                self._element,
                style
            )
        except Exception as e:
            self.error_log("highlight exception: %s" % str(e))

        sleep(highlight_time)

        try:
            driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                self._element,
                original_style
            )
        except Exception as e:
            self.error_log("highlight exception: %s" % str(e))

        return True

    def scroll_into_view(self, **kwargs):
        self.debug_log("Scrolling into view element")

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )
        try:
            self.pdriver.execute_script(
                "arguments[0].scrollIntoView()",
                self._element
            )

        except (
                exceptions.WebDriverException,
                exceptions.StaleElementReferenceException
                ) as e:
            if raise_exception:
                raise
            else:
                tb = traceback.format_exc()
                self.error_log('scroll_into_view WebDriverException: %s' % tb)
                return False

        return True

    def select_all(self, **kwargs):
        self.debug_log("Selecting all in element")

        raise_exception = kwargs.get(
            'raise_exception',
            BROME_CONFIG['proxy_driver']['raise_exception']
        )

        # http://stackoverflow.com/questions/985272/selecting-text-in-an-element-akin-to-highlighting-with-your-mouse  # noqa
        try:
            self.pdriver.execute_script("""
                var element = arguments[0],
                    range, selection;

                if (document.body.createTextRange) {
                    range = document.body.createTextRange();
                    range.moveToElementText(element);
                    range.select();
                } else if (window.getSelection) {
                    selection = window.getSelection();
                    range = document.createRange();
                    range.selectNodeContents(element);
                    selection.removeAllRanges();
                    selection.addRange(range);
                }
            """, self._element)
        except exceptions.WebDriverException:
            if raise_exception:
                raise
            else:
                tb = traceback.format_exc()
                self.error_log('select_all WebDriverException: %s' % tb)
                return False

        return True

    def hover(self, **kwargs):
        self.debug_log("Hovering element")

        try:
            ActionChains(self.pdriver)\
                .move_to_element(self._element)\
                .perform()
        except exceptions.WebDriverException:
            tb = traceback.format_exc()
            self.error_log('hover WebDriverException: %s' % tb)
            return False

        return True
