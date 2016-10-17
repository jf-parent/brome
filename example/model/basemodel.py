
import sys


class BaseModel(object):

    def info(self, msg):
        self.pdriver.info_log(
            self.info_format.format(
                self=self,
                msg=msg
            )
        )

    def debug(self, msg):
        self.pdriver.debug_log(
            self.info_format.format(
                self=self,
                msg=msg
            )
        )

    def bind_root_xpath(self, func, selector=None, *args, **kwargs):
        if selector:
            effective_selector = [self.get_root_xpath(), selector]
        else:
            effective_selector = self.get_root_xpath()
        msg = 'Calling {func}: selector = {selector}, args: {args},'\
            'kwargs: {kwargs}'
        self.debug(
            msg
            .format(
                func=func,
                selector=effective_selector,
                args=args,
                kwargs=kwargs
            )
        )

        return getattr(self.pdriver, func)(effective_selector, *args, **kwargs)

    def find(self, selector=None, *args, **kwargs):
        func = sys._getframe().f_code.co_name
        return self.bind_root_xpath(func, selector, *args, **kwargs)

    def assert_present(self, selector=None, *args, **kwargs):
        func = sys._getframe().f_code.co_name
        return self.bind_root_xpath(func, selector, *args, **kwargs)

    def assert_visible(self, selector=None, *args, **kwargs):
        func = sys._getframe().f_code.co_name
        return self.bind_root_xpath(func, selector, *args, **kwargs)

    def assert_not_visible(self, selector=None, *args, **kwargs):
        func = sys._getframe().f_code.co_name
        return self.bind_root_xpath(func, selector, *args, **kwargs)

    def is_present(self, selector=None, *args, **kwargs):
        func = sys._getframe().f_code.co_name
        return self.bind_root_xpath(func, selector, *args, **kwargs)
