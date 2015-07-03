
from brome.core.models.utils import *

class ProxyElement(object):
    
    def __init__(self, element, selector):
        self._element = element
        self.selector = selector
    
    def __getattr__(self, funcname):
        print 'proxyelement'
        return getattr(self._element, funcname)

    def click(self):
        print 'proxyelement click'

        self.highlight(style = 'gb')

        self._element.click()

    def clear(self):
        pass

    def highlight(self, **kwargs):
        """
            kwargs:
                style: string; default: 'yr'
                highlight_time: int; default: .3
        """
        style = kwargs.get('style', 'yr')
        highlight_time = kwargs.get('highlight_time', .3)

        #TODO configurable
        style_dict = {}
        style_dict['yr'] = "background: yellow; border: 2px solid red;"
        style_dict['rb'] = "background: red; border: 2px solid black;"
        style_dict['gb'] = "background: green; border: 2px solid black;"
        style_dict['pb'] = "background: purple; border: 2px solid black;"

        driver = self._element._parent

        try:
            original_style = self._element.get_attribute('style')

            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", self._element, style_dict[style])
        except StaleElementReferenceException:
            return False

        sleep(highlight_time)

        try:
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", self._element, original_style)
        except StaleElementReferenceException:
            return False
