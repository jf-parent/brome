Assertion
=========

All assert function return a boolean: True if the assertion succeed; False otherwise.

If you gave a test dictionary to the Brome object in the bro executable then you can give a test id to the assert function so it can save the test result for you::

    test_dict = {}
    test_dict['#1'] = "The login button is visible"
    test_dict['#2'] = {
        'name': 'Test',
        'embed': False
    }

    brome = Brome(
        config_path = os.path.join(HERE, "config", "brome.yml"),
        selector_dict = selector_dict,
        test_dict = test_dict, # <-- this dict
        browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"),
        absolute_path = HERE
    )

So later in your code you can do this::

    pdriver.assert_visible("sv:login_button", '#1')
    >>>True

Or if you prefer you can write the test description inline instead::

    pdriver.assert_visible("sv:login_button", 'The login button is visible')
    >>>True

If you don't want this assertion to be saved then use the assert function like this::

    
    pdriver.assert_visible("sv:login_button")
    >>>True

Assertion function never raise an exception.

The following config affect the fonctionality of assert functions:

* `runner:embed_on_assertion_success`
* `runner:embed_on_assertion_failure`
* `runner:play_sound_on_assertion_success`
* `runner:play_sound_on_assertion_failure`
* `proxy_driver:take_screenshot_on_assertion_failure`
* `proxy_driver:take_screenshot_on_assertion_success`

If you have a bug that won't be fixed anytime soon and your config `runner:embed_on_assertion_failure` is set to True then you can change your test_dict like so to stop embed on this particular test::

    test_dict['#2'] = {
        'name': 'Test',
        'embed': False
    }

Assertion functions
~~~~~~~~~~~~~~~~~~~

Here is the list of all assert function found in the `pdriver`:

Assert present
--------------

This will assert that the element is present in the dom::

    assert_present(selector, "#2")

    assert_present(selector, "#2", wait_until_present = False)

    assert_present(selector, "#2", wait_until_present = True)

* The default for the `wait_until_present` kwargs is `proxy_driver:wait_until_present_before_assert_present`.

Assert not present
------------------

This will assert that the element is not present in the dom::

    assert_not_present(selector, "#2")

    assert_not_present(selector, "#2", wait_until_not_present = True)

    assert_not_present(selector, "#2", wait_until_not_present = False)

* The default for the `wait_until_not_present` kwargs is `proxy_driver:wait_until_not_present_before_assert_not_present`.

Assert visible
--------------

This will assert that the element is visible in the dom::

    assert_visible(selector, "#2")

    assert_visible(selector, "#2", highlight = False)

    assert_visible(selector, "#2", wait_until_visible = False)

* The default for the `wait_until_visible` kwargs is `proxy_driver:wait_until_visible_before_assert_visible`.
* The default for the `highlight` kwargs is `proxy_driver:highlight_on_assertion_success`.
* The highlight style is configurable with the config `highlight:style_on_assertion_success`.

Assert not visible
------------------

This will assert that the element is not visible in the dom::

    assert_not_visible(selector, "#2")

    assert_not_visible(selector, "#2", highlight = False)

    assert_not_visible(selector, "#2", wait_until_not_visible = False)

* The default for the `wait_until_not_visible` kwargs is `proxy_driver:wait_until_not_visible_before_assert_not_visible`.
* The default for the `highlight` kwargs is `proxy_driver:highlight_on_assertion_failure`.
* The highlight style is configurable with the config `highlight:style_on_assertion_failure`.

Assert text equal
-----------------

This will assert that the element's test is equal to the given value::

    assert_text_equal("sv:username_input", "user", "#2")

    pdriver.assert_text_equal("sv:username_input", "error", '#2', highlight = False)

    pdriver.assert_text_equal("sv:username_input", "error", '#2', wait_until_visible = False)

* The default for the `wait_until_visible` kwargs is `proxy_driver:wait_until_visible_before_assert_visible`.
* The default for the `highlight` kwargs is `proxy_driver:highlight_on_assertion_success`.
* The highlight style is configurable with the config `highlight:style_on_assertion_success`.
* The highlight style is configurable with the config `highlight:style_on_assertion_failure`.

Assert text not equal
---------------------

This will assert that the element's test is not equal to the given value::

    pdriver.assert_text_not_equal("sv:username_input", "error", '#2')

    pdriver.assert_text_not_equal("sv:username_input", "error", '#2', highlight = False)

    pdriver.assert_text_not_equal("sv:username_input", "error", '#2', wait_until_visible = False)

* The default for the `wait_until_visible` kwargs is `proxy_driver:wait_until_visible_before_assert_visible`.
* The default for the `highlight` kwargs is `proxy_driver:highlight_on_assertion_success`.
* The highlight style is configurable with the config `highlight:style_on_assertion_success`.
* The highlight style is configurable with the config `highlight:style_on_assertion_failure`.
