#! -*- coding: utf-8 -*-

import traceback

from brome.core.model.utils import *

class ProxyElement(object):
    
    def __init__(self, element, selector, pdriver):
        self._element = element
        self.selector = selector
        self.pdriver = pdriver
    
    def __getattr__(self, funcname):
        return getattr(self._element, funcname)

    def error_log(self, msg):
        self.pdriver.error_log("[%s] %s"%(repr(self), msg))

    def debug_log(self, msg):
        self.pdriver.error_log("[%s] %s"%(repr(self), msg))

    def __repr__(self):
        msg = ["WebElement (selector: '%s')"%self.selector]

        if self._element.get_attribute('id'):
            msg.append("(id: '%s')"%self._element.get_attribute('id'))
        
        if self._element.get_attribute('name'):
            msg.append("(name: '%s')"%self._element.get_attribute('name'))

        if self._element.get_attribute('class'):
            msg.append("(class: '%s')"%self._element.get_attribute('class'))

        return ' '.join(msg)

    def is_displayed(self, **kwargs):
        self.debug_log("Is displayed")

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.pdriver.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        retry = kwargs.get('retry', True)

        try:
            is_displayed = self._element.is_displayed()
            self.debug_log("is displayed")
            return is_displayed
        except StaleElementReferenceException:
            if retry:
                #NOTE this is an imperfect solution since we can have found the element with find_last
                #TODO find a better way to handle this edge case
                self.debug_log("StaleElementReferenceException; retrying...")
                self._element = self.pdriver.find(self.selector, raise_exception = False)
                if self._element:
                    return self.is_displayed(retry = False)
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
                            self.pdriver.get_config_value(
                                'highlight:highlight_when_element_is_clicked'
                            )
                    )
        wait_until_clickable = kwargs.get(
                            'wait_until_clickable',
                            self.pdriver.get_config_value(
                                'proxy_element:wait_until_clickable'
                            )
                    )

        if wait_until_clickable:
            #TODO manage the raise exception better
            self.pdriver.wait_until_clickable(self.selector, raise_exception = True)

        if highlight:
            self.highlight(
                style = self.pdriver.get_config_value(
                            'highlight:style_when_element_is_clicked'
                        )
                )

        try:
            self._element.click()
        except (InvalidElementStateException, WebDriverException) as e:
            self.debug_log("click exception: %s"%str(e))
            sleep(2)
            self._element.click()
        except StaleElementReferenceException as e:
            self.debug_log("click exception StaleElementReferenceException: %s"%str(e))
            sleep(2)
            self._element = self.pdriver.find(self.selector)
            self._element.click()

        return True

    def send_keys(self, value, **kwargs):
        self.debug_log("Sending keys")

        highlight = kwargs.get( 
                            'highlight',
                            self.pdriver.get_config_value(
                                'highlight:highlight_when_element_receive_keys'
                            )
                    )
        wait_until_clickable = kwargs.get(
                            'wait_until_clickable',
                            self.pdriver.get_config_value(
                                'proxy_element:wait_until_clickable'
                            )
                    )

        if wait_until_clickable:
            #TODO manage the raise exception better
            self.pdriver.wait_until_clickable(self.selector, raise_exception = True)

        if highlight:
            self.highlight(
                style = self.pdriver.get_config_value(
                            'highlight:style_when_element_receive_keys'
                        )
            )

        clear = kwargs.get('clear', False)

        if clear:
            self.clear()

        try:
            self._element.send_keys(value)
        except StaleElementReferenceException as e:
            self.debug_log("send_keys exception StaleElementReferenceException: %s"%str(e))
            sleep(2)
            self._element = self.pdriver.find(self.selector)
            self._element.send_keys(value)
        except (InvalidElementStateException, WebDriverException) as e:
            self.debug_log("send_keys exception: %s"%str(e))
            sleep(2)
            self._element.send_keys(value)

        return True

    def clear(self):
        self.debug_log("Clearing element")

        try:
            self._element.clear()
        except (InvalidElementStateException, WebDriverException) as e:
            self.debug_log("send_keys exception: %s"%str(e))
            sleep(2)
            self._element.clear()
        except StaleElementReferenceException as e:
            self.debug_log("send_keys exception StaleElementReferenceException: %s"%str(e))
            sleep(2)
            self._element = self.pdriver.find(self.selector)
            self._element.clear()

        return True

    def highlight(self, **kwargs):
        self.debug_log("Highlighting element")
        """
            kwargs:
                style: css
                highlight_time: int; default: .3
        """
        style = kwargs.get('style')
        highlight_time = kwargs.get('highlight_time', .3)

        driver = self._element._parent

        try:
            original_style = self._element.get_attribute('style')

            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", self._element, style)
        except StaleElementReferenceException:
            return False

        sleep(highlight_time)

        try:
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", self._element, original_style)
        except StaleElementReferenceException:
            return False

        return True

    def scroll_into_view(self, **kwargs):
        self.debug_log("Scrolling into view element")

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.pdriver.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )
        try:
            self.pdriver.execute_script("arguments[0].scrollIntoView()", self._element)

        except WebDriverException as e:
            if raise_exception:
                raise
            else:
                tb = traceback.format_exc()
                self.error_log('scroll_into_view WebDriverException: %s'%str(tb))
                return False

        return True

    def select_all(self, **kwargs):
        self.debug_log("Selecting all in element")

        raise_exception = kwargs.get(
                                    'raise_exception',
                                    self.pdriver.get_config_value(
                                        'proxy_driver:raise_exception'
                                    )
                                )

        #http://stackoverflow.com/questions/985272/selecting-text-in-an-element-akin-to-highlighting-with-your-mouse
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
        except WebDriverException:
            if raise_exception:
                raise
            else:
                tb = traceback.format_exc()
                self.error_log('select_all WebDriverException: %s'%str(tb))
                return False

        return True
