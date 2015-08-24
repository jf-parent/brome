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

    def click(self, **kwargs):
        
        highlight = kwargs.get( 
                            'highlight',
                            self.pdriver.get_config_value(
                                'highlight:highlight_when_element_is_clicked'
                            )
                    )

        if highlight:
            self.highlight(
                style = self.pdriver.get_config_value(
                            'highlight:style_when_element_is_clicked'
                        )
                )

        self._element.click()

        return True

    def send_keys(self, value, **kwargs):
        highlight = kwargs.get( 
                            'highlight',
                            self.pdriver.get_config_value(
                                'highlight:highlight_when_element_receive_keys'
                            )
                    )

        if highlight:
            self.highlight(
                style = self.pdriver.get_config_value(
                            'highlight:style_when_element_receive_keys'
                        )
            )

        clear = kwargs.get('clear', False)

        if clear:
            self.clear()

        self._element.send_keys(value)

        return True

    def clear(self):
        self._element.clear()

        return True

    def highlight(self, **kwargs):
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
