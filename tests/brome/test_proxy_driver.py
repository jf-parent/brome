from time import sleep

from pytest import set_trace  # noqa
from selenium.common import exceptions

from brome.core.selector import Selector
from brome_config import default_config, default_browser_config
from model.basetest import BaseTest
from model.selector import selector_dict
from model.test_dict import test_dict
from model.user import User
from brome.runner.local_runner import LocalRunner


def test_wait_until_visible(browser_name, brome):
    class TestWaitUntilVisible(object):
        class Test(BaseTest):

            name = 'Wait until visible'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_visible_test")

                element = self.pdriver.find(
                    "id:2",
                    wait_until_present=False,
                    wait_until_visible=False,
                    raise_exception=False
                )

                assert not element

                element = self.pdriver.find(
                    "id:2",
                    wait_until_visible=True,
                    raise_exception=False
                )

                assert element

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestWaitUntilVisible]
    )
    LocalRunner(brome).execute()


def test_wait_until_present(browser_name, brome):
    class TestWaitUntilPresent(object):
        class Test(BaseTest):

            name = 'Wait until present'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_present_test")

                el = self.pdriver.wait_until_present("id:3")
                assert el.get_attribute('id') == '3'

                el = self.pdriver.wait_until_present(
                    "id:1",
                    raise_exception=False,
                    timeout=6
                )
                assert el.get_attribute('id') == '1'

                el = self.pdriver.wait_until_present(
                    "id:2",
                    raise_exception=False
                )
                assert not el

                el = self.pdriver.wait_until_present(
                    "id:2",
                    raise_exception=False,
                    timeout=11
                )
                assert el.get_attribute('id') == '2'

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestWaitUntilPresent]
    )
    LocalRunner(brome).execute()


def test_wait_until_not_visible(browser_name, brome):
    class TestWaitUntilNotVisible(object):
        class Test(BaseTest):

            name = 'Wait until not visible'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_not_visible_test")

                self.pdriver.wait_until_not_visible(
                    "id:2",
                    raise_exception=False
                )

                element = self.pdriver.find("id:2", raise_exception=False)

                assert not element

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestWaitUntilNotVisible]
    )
    LocalRunner(brome).execute()


def test_wait_until_not_present(browser_name, brome):
    class TestWaitUntilNotPresent(object):
        class Test(BaseTest):
            name = 'Wait until not present'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_not_present_test")

                ret = self.pdriver.wait_until_not_present(
                    "id:3",
                    raise_exception=False
                )
                assert ret

                ret = self.pdriver.wait_until_not_present(
                    "id:4",
                    raise_exception=False
                )
                assert not False

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestWaitUntilNotPresent]
    )
    LocalRunner(brome).execute()


def test_state(browser_name, brome):
    class UnStateful(object):
        pass

    class TestState(object):
        class Test(BaseTest):

            name = 'State'

            def create_state(self):
                self.unstateful = UnStateful()
                self.stateful = User(self.pdriver, 'test')
                self.int_ = 1
                self.float_ = 0.1
                self.unicode_ = u'test'
                self.str_ = 'str'
                self.list_ = [1, 2]
                self.dict_ = {'key': 1}

            def run(self, **kwargs):

                self.info_log("Running...")

                # TODO find a way to the load the state before asserting
                # assert not hasattr(self, 'unstateful')

                assert hasattr(self, 'stateful')

                assert hasattr(self, 'int_')

                assert hasattr(self, 'float_')

                assert hasattr(self, 'unicode_')

                assert hasattr(self, 'str_')

                assert hasattr(self, 'list_')

                assert hasattr(self, 'dict_')

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestState]
    )
    LocalRunner(brome).execute()


def test_selector(browser_name, brome):
    class TestSelector(object):
        class Test(BaseTest):

            name = 'Selector'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("selector_test")

                # ##TAG NAME
                # FIND ALL BY TAG NAME
                elements = self.pdriver.find_all("tn:h1")
                assert len(elements) == 2

                # FIND BY TAG NAME
                element = self.pdriver.find("tn:h1")
                assert element.get_attribute('id') == '1'

                # FIND LAST BY TAG NAME
                element = self.pdriver.find_last("tn:h1")
                assert element.get_attribute('id') == '2'

                # FIND BY TAG NAME DOESNT EXIST
                element = self.pdriver.find(
                    "tn:thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY TAG NAME DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "tn:thisdoesntexist",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##NAME
                # FIND ALL BY NAME
                elements = self.pdriver.find_all("nm:name-selector")
                assert len(elements) == 2

                # FIND BY NAME
                element = self.pdriver.find("nm:name-selector")
                assert element.get_attribute('id') == '3'

                # FIND LAST BY NAME
                element = self.pdriver.find_last("nm:name-selector")
                assert element.get_attribute('id') == '4'

                # FIND BY NAME DOESNT EXIST
                element = self.pdriver.find(
                    "nm:thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY NAME DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "nm:thisdoesntexist",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##CLASS NAME
                # FIND ALL BY CLASS NAME
                elements = self.pdriver.find_all("cn:class-selector")
                assert len(elements) == 2

                # FIND BY CLASS NAME
                element = self.pdriver.find("cn:class-selector")
                assert element.get_attribute('id') == '2'

                # FIND LAST BY CLASS NAME
                element = self.pdriver.find_last("cn:class-selector")
                assert element.get_attribute('id') == '5'

                # FIND BY CLASS NAME DOESNT EXIST
                element = self.pdriver.find(
                    "cn:thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False
                )
                assert not element

                # FIND BY CLASS NAME DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "cn:thisdoesntexist",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##ID
                # FIND ALL BY ID
                elements = self.pdriver.find_all("id:1")
                assert len(elements) == 1

                # FIND BY ID
                element = self.pdriver.find("id:1")
                assert element.get_attribute('id') == '1'

                # FIND LAST BY ID
                element = self.pdriver.find_last("id:1")
                assert element.get_attribute('id') == '1'

                # FIND BY ID DOESNT EXIST
                element = self.pdriver.find(
                    "id:thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False
                )
                assert not element

                # FIND BY ID DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "id:thisdoesntexist",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##XPATH
                # FIND ALL BY XPATH
                elements = self.pdriver.find_all("xp://h1")
                assert len(elements) == 2

                # FIND BY XPATH
                element = self.pdriver.find("xp://*[@id = 1]")
                assert element.get_attribute('id') == '1'

                # FIND LAST BY XPATH
                element = self.pdriver.find_last("xp://h1")
                assert element.get_attribute('id') == '2'

                # FIND BY XPATH DOESNT EXIST
                element = self.pdriver.find(
                    "xp://*[@class = 'thisdoesntexist']",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY XPATH DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "xp://*[@class = 'thisdoesntexist']",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##CSS
                # FIND ALL BY CSS
                elements = self.pdriver.find_all("cs:h1")
                assert len(elements) == 2

                # FIND BY CSS
                element = self.pdriver.find("cs:h1")
                assert element.get_attribute('id') == '1'

                # FIND LAST BY CSS
                element = self.pdriver.find_last("cs:h1")
                assert element.get_attribute('id') == '2'

                # FIND BY CSS DOESNT EXIST
                element = self.pdriver.find(
                    "cs:.thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY CSS DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "cs:.thisdoesntexist",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##LINK TEXT
                # FIND ALL BY LINK TEXT
                elements = self.pdriver.find_all("lt:link-text-selector")
                assert len(elements) == 2

                # FIND BY LINK TEXT
                element = self.pdriver.find("lt:link-text-selector")
                assert element.get_attribute('id') == '6'

                # FIND LAST BY LINK TEXT
                element = self.pdriver.find_last("lt:link-text-selector")
                assert element.get_attribute('id') == '7'

                # FIND BY LINK TEXT DOESNT EXIST
                element = self.pdriver.find(
                    "lt:text-selector",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY LINK TEXT DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "lt:thisdoesntexit",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##PARTIAL LINK TEXT
                # FIND ALL BY PARTIAL LINK TEXT
                elements = self.pdriver.find_all("pl:text-selector")
                assert len(elements) == 2

                # FIND BY PARTIAL LINK TEXT
                element = self.pdriver.find("pl:text-selector")
                assert element.get_attribute('id') == '6'

                # FIND LAST BY PARTIAL LINK TEXT
                element = self.pdriver.find_last("pl:text-selector")
                assert element.get_attribute('id') == '7'

                # FIND BY PARTIAL LINK TEXT DOESNT EXIST
                element = self.pdriver.find(
                    "pl:thisdoesntexist",
                    raise_exception=False,
                    wait_until_visible=False,
                    wait_until_present=False
                )
                assert not element

                # FIND BY PARTIAL LINK TEXT DOESNT EXIST RAISE EXCEPTION
                try:
                    self.pdriver.find(
                        "pl:thisdoesntexit",
                        wait_until_visible=False,
                        wait_until_present=False
                    )
                    assert False
                except exceptions.NoSuchElementException:
                    assert True

                # ##SELECTOR VARIABLE
                # Selector variable that doesnt exist in the selector dict
                selector = "sv:not_exist"
                try:
                    Selector(self.pdriver, selector)
                    assert False
                except:
                    assert True

                # Selector variable that are invalid
                # selector_dict['test_2'] = "zz://*[@id = '1']"
                selector = "sv:test_2"
                try:
                    Selector(self.pdriver, selector)
                    assert False
                except:
                    assert True

                # Single selector
                selector = "sv:test_1"
                _selector = Selector(self.pdriver, selector)

                assert _selector.get_selector() == selector_dict["test_1"][3:]

                # Double selector
                selector_1 = "sv:test_3"
                selector_2 = "sv:test_4"
                _selector = Selector(self.pdriver, [selector_1, selector_2])

                assert _selector.get_selector() == selector_dict["test_3"][3:] + selector_dict["test_4"][3:]  # noqa

                # Multiple selector
                selector_1 = "sv:test_3"
                selector_2 = "sv:test_4"
                selector_3 = "sv:test_5"
                _selector = Selector(self.pdriver, [selector_1, selector_2, selector_3])  # noqa

                assert _selector.get_selector() == selector_dict["test_3"][3:] + selector_dict["test_4"][3:] + selector_dict["test_5"][3:]  # noqa

                # Multiple selector with mismatch
                selector_1 = "sv:test_3"
                selector_2 = "sv:test_7"
                try:
                    Selector(self.pdriver, [selector_1, selector_2])
                    assert False
                except:
                    assert True

                # Selector browser specific
                self.app.pdriver._driver.capabilities['browserName'] = 'firefox'  # noqa

                _selector = Selector(self.pdriver, 'sv:example_multiple_selector')  # noqa

                assert _selector.get_selector() == selector_dict['example_multiple_selector']['default'][3:]  # noqa

                self.app.pdriver._driver.capabilities['browserName'] = 'chrome'

                _selector = Selector(self.pdriver, 'sv:example_multiple_selector')  # noqa

                assert _selector.get_selector() == selector_dict['example_multiple_selector']['chrome|iphone|android'][3:]  # noqa

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestSelector]
    )
    LocalRunner(brome).execute()


def test_select_all(browser_name, brome):
    class TestSelectAll(object):
        class Test(BaseTest):
            name = 'Select all'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("select_all_test")

                self.pdriver.find("id:selectme").select_all()

                # TODO find a way to know that the text has been selected

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestSelectAll]
    )
    LocalRunner(brome).execute()


def test_assert_wait_until_visible(browser_name, brome):
    class TestAssertWaitUntilVisible(object):
        class Test(BaseTest):
            name = 'Is visible'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_visible_test")

                ret = self.pdriver.is_visible("id:3")
                assert ret

                ret = self.pdriver.is_visible("id:1")
                assert not ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertWaitUntilVisible]
    )
    LocalRunner(brome).execute()


def test_assert_wait_until_present(browser_name, brome):
    class TestAssertWaitUntilPresent(object):
        class Test(BaseTest):
            name = 'Is present'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_present_test")

                ret = self.pdriver.is_present("id:2")
                assert not ret

                ret = self.pdriver.is_present("id:3")
                assert ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertWaitUntilPresent]
    )
    LocalRunner(brome).execute()


def test_assert_intercept_javascript_error_disabled(browser_name, brome):
    class TestAssertInterceptJavascriptErrorDisabled(object):
        class Test(BaseTest):

            name = 'Intercept javascript error disabled'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to('intercept_javascript_error_test')

                js_error = self.pdriver.get_javascript_error(
                    return_type='list'
                )
                assert js_error == []

                js_error = self.pdriver.get_javascript_error(
                    return_type='string'
                )
                assert js_error == []

                self.pdriver.find("id:error-btn").click()
                sleep(2)

                js_error = self.pdriver.get_javascript_error(
                    return_type='list'
                )
                assert js_error == []

                self.pdriver.find("id:error-btn").click()
                sleep(2)

                js_error = self.pdriver.get_javascript_error(
                    return_type='string'
                )
                assert js_error == []

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name
    brome_config['proxy_driver']['intercept_javascript_error'] = False

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertInterceptJavascriptErrorDisabled]
    )
    LocalRunner(brome).execute()


def test_assert_intercept_javascript_error(browser_name, brome):
    class TestAssertInterceptJavascriptError(object):
        class Test(BaseTest):

            name = 'Intercept javascript error'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to('intercept_javascript_error_test')

                js_error = self.pdriver.get_javascript_error(
                    return_type='list'
                )
                assert js_error == []

                js_error = self.pdriver.get_javascript_error(
                    return_type='string'
                )
                assert js_error == self.pdriver.no_javascript_error_string

                self.pdriver.find("id:error-btn").click()
                sleep(2)

                js_error = self.pdriver.get_javascript_error(
                    return_type='list'
                )
                assert len(js_error) > 0

                self.pdriver.find("id:error-btn").click()
                sleep(2)

                js_error = self.pdriver.get_javascript_error(
                    return_type='string'
                )
                assert js_error != self.pdriver.no_javascript_error_string

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name
    brome_config['proxy_driver']['intercept_javascript_error'] = True

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertInterceptJavascriptError]
    )
    LocalRunner(brome).execute()


def test_assert_inject_script(browser_name, brome):
    class TestAssertInjectScript(object):
        class Test(BaseTest):
            name = 'Inject script'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("select_all_test")

                """
                try:
                    ret = self.pdriver.execute_script(
                        "return module_test.test;"
                    )
                    assert False
                except WebDriverException:
                    assert True
                """

                self.pdriver.inject_js_script("/static/test_script.js")
                sleep(2)

                ret = self.pdriver.execute_script("return module_test.test;")
                assert ret == 'test'

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertInjectScript]
    )
    LocalRunner(brome).execute()


def test_assert_dnd(browser_name, brome):
    class TestAssertDnd(object):
        class Test(BaseTest):
            name = 'Drag and Drop'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.pdriver.get("http://touchpunch.furf.com/content.php?/droppable/default-functionality")  # noqa

                self.app.pdriver.drag_and_drop(
                    "id:draggable",
                    "id:droppable"
                )

                ret = self.app.pdriver.assert_visible(
                    "xp://p[contains(text(), 'Dropped!')]"
                )
                assert ret

                # TODO investigate and fix
                """
                self.app.go_to("dnd_test")

                self.app.pdriver.drag_and_drop(
                    "id:column-a",
                    "id:column-b"
                )

                els = self.app.pdriver.find_all("cn:column")
                assert els[0].get_attribute('id') == "column-b"
                """

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertDnd]
    )
    LocalRunner(brome).execute()


def test_assert_click(browser_name, brome):
    class TestAssertClick(object):
        class Test(BaseTest):
            name = 'Click'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("click_test")

                element = self.pdriver.find("id:1")

                element.click()

                result = self.pdriver.find(
                    "xp://*[contains(text(), 'clicked')]"
                )

                assert result

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertClick]
    )
    LocalRunner(brome).execute()


def test_assert_visible(browser_name, brome):
    class TestAssertVisible(object):
        class Test(BaseTest):

            name = 'Assert visible'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("wait_until_visible_test")

                ret = self.pdriver.assert_visible(
                    "id:2",
                    wait_until_visible=False
                )
                assert not ret

                ret = self.pdriver.assert_visible(
                    "id:2",
                    wait_until_visible=True
                )
                assert ret

                ret = self.pdriver.assert_visible("id:3")
                assert ret

                ret = self.pdriver.assert_visible("id:1")
                assert not ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertVisible]
    )
    LocalRunner(brome).execute()


def test_assert_equal_not_equal(browser_name, brome):
    class TestAssertEqualNotEqual(object):
        class Test(BaseTest):
            name = 'Assert equal and not equal'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("assert_text_test")

                ret = self.app.pdriver.assert_text_equal(
                    "id:1",
                    "this is visible"
                )
                assert ret

                ret = self.app.pdriver.assert_text_not_equal(
                    "id:1",
                    "whatever"
                )
                assert ret

                ret = self.app.pdriver.assert_text_not_equal(
                    "id:1",
                    "this is visible"
                )
                assert not ret

                ret = self.app.pdriver.assert_text_equal("id:1", "whatever")
                assert not ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertEqualNotEqual]
    )
    LocalRunner(brome).execute()


def test_assert_present(browser_name, brome):
    class TestAssertPresent(object):
        class Test(BaseTest):
            name = 'Assert present'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("assert_present_test")

                ret = self.pdriver.assert_present(
                    "id:2",
                    wait_until_present=False
                )
                assert not ret

                ret = self.pdriver.assert_present("id:3")
                assert ret

                ret = self.pdriver.assert_present(
                    "id:2",
                    wait_until_present=True
                )
                assert ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertPresent]
    )
    LocalRunner(brome).execute()


def test_assert_not_visible(browser_name, brome):
    class TestAssertNotVisible(object):
        class Test(BaseTest):

            name = 'Assert not visible'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("assert_not_visible_test")

                ret = self.pdriver.assert_not_visible("id:2")
                assert ret

                self.app.go_to("assert_not_visible_test")

                ret = self.pdriver.assert_not_visible(
                    "id:3",
                    wait_until_not_visible=False
                )
                assert not ret

                self.app.go_to("assert_not_visible_test")

                ret = self.pdriver.assert_not_visible(
                    "id:3",
                    wait_until_not_visible=True
                )
                assert ret

                ret = self.pdriver.assert_not_visible("id:2")
                assert not ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertNotVisible]
    )
    LocalRunner(brome).execute()


def test_assert_not_present(browser_name, brome):
    class TestAssertNotPresent(object):
        class Test(BaseTest):

            name = 'Assert not present'

            def run(self, **kwargs):

                self.info_log("Running...")

                self.app.go_to("assert_not_present_test")

                ret = self.pdriver.assert_not_present(
                    "id:3",
                    wait_until_not_present=False
                )
                assert not ret

                self.app.go_to("assert_not_present_test")

                ret = self.pdriver.assert_not_present(
                    "id:2",
                    wait_until_not_present=False
                )
                assert ret

                self.app.go_to("assert_not_present_test")

                ret = self.pdriver.assert_not_present(
                    "id:3",
                    wait_until_not_present=True
                )
                assert ret

    brome_config = default_config.copy()
    brome_config['runner']['localhost_runner'] = browser_name

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=default_browser_config,
        tests=[TestAssertNotPresent]
    )
    LocalRunner(brome).execute()
