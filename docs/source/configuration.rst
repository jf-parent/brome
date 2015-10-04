Configuration
=============

Here is all the configuration options that brome support. You have to provide a yaml configuration file to brome when you create it. This step is already done in the bro executable::
    
    brome = Brome(
        config_path = os.path.join(HERE, "config", "brome.yml"), #<--- this file
        selector_dict = selector_dict,
        test_dict = test_dict,
        browsers_config_path = os.path.join(HERE, "config", "browsers_config.yml"),
        absolute_path = HERE
    )

Inside the brome.yml configuration file is a bunch of section with options. You can control the behavior the runner, the proxy driver, the proxy element, put some custom project config, etc... Below is a break down of each of the brome configuration options.

sample configuration file
-------------------------

::

    saucelabs:
      username: ''
      key: ''
    browser:
      maximize_window: false
      window_height: 725
      window_width: 1650
      window_x_position: 0
      window_y_position: 0
    database:
      sqlalchemy.url: 'sqlite:///unittest.db'
    ec2:
      wait_after_instance_launched: 30
      wait_until_system_and_instance_check_performed: true
    grid_runner:
      kill_selenium_server: true
      max_running_time: 7200
      selenium_hub_config: '/resources/hub-config.json'
      selenium_server_command: 'java -jar {selenium_server_jar_path} -role hub -hubConfig {selenium_hub_config} -DPOOL_MAX 512 &'
      selenium_server_ip: 'localhost'
      selenium_server_jar_path: '/resources/selenium-server-standalone.jar'
      selenium_server_port: 4444
      start_selenium_server: false
    highlight:
      highlight_on_assertion_failure: true
      highlight_on_assertion_success: true
      highlight_when_element_is_clicked: true
      highlight_when_element_is_visible: true
      highlight_when_element_receive_keys: true
      style_on_assertion_failure: 'background: red; border: 2px solid black;'
      style_on_assertion_success: 'background: green; border: 2px solid black;'
      style_when_element_is_clicked: 'background: yellow; border: 2px solid red;'
      style_when_element_is_visible: 'background: purple; border: 2px solid black;'
      style_when_element_receive_keys: 'background: yellow; border: 2px solid red;'
      use_highlight: true
    logger_runner:
      filelogger: false
      format: "[%(batchid)s]\e[32m%(message)s\e[0m"
      level: 'INFO'
      streamlogger: true
    logger_test:
      filelogger: false
      format: "[%(batchid)s]\e[34m(%(testname)s)\e[0m:\e[32m%(message)s\e\[0m"
      level: 'INFO'
      streamlogger: true
    project:
      test_batch_result_path: false
      url: 'http://localhost:7777'
    proxy_driver:
      use_javascript_dnd: true
      default_timeout: 5
      intercept_javascript_error: true
      raise_exception: true
      take_screenshot_on_assertion_failure: true
      take_screenshot_on_assertion_success: false
      validate_css_selector: true
      validate_xpath_selector: true
      wait_until_not_present_before_assert_not_present: true
      wait_until_not_visible_before_assert_not_visible: true
      wait_until_present_before_assert_present: true
      wait_until_present_before_find: true
      wait_until_visible_before_assert_visible: true
      wait_until_visible_before_find: true
    runner:
      cache_screenshot: true
      embed_on_assertion_failure: false
      embed_on_assertion_success: false
      embed_on_test_crash: false
      play_sound_on_assertion_failure: false
      play_sound_on_assertion_success: false
      play_sound_on_ipython_embed: false
      play_sound_on_pdb: false
      play_sound_on_test_crash: false
      play_sound_on_test_finished: false
      sound_on_assertion_failure: '{testid} failed'
      sound_on_assertion_success: '{testid} succeeded'
      sound_on_ipython_embed: 'Attention required'
      sound_on_pdb: 'Attention required'
      sound_on_test_crash: 'Crash'
      sound_on_test_finished: 'Test finished'
    webserver:
      open_browser: false
      ASSETS_DEBUG: true
      CACHE_TYPE: 'simple'
      CLOSED_REGISTRATION: false
      DEBUG: false
      DEBUG_TB_ENABLED: false
      DEBUG_TB_INTERCEPT_REDIRECTS: false
      HOST: 'localhost'
      PORT: 5000
      REGISTRATION_TOKEN: ''
      SECRET_KEY: ''
      SHOW_TEST_INSTANCES: true
      SHOW_VIDEO_CAPTURE: true
      filelogger: false
      level: 'INFO'
      streamlogger: false

project
-------

* **test_batch_result_path**: The test path where the test batch result file will be create. If you don't want to save any file when a test batch run, just set this options to False. `str [path] | bool (false only)` `(default: '')`

* **url**: The url of the server on which the test run (must include the protocol) e.g.:https://the-internet.herokuapp.com/ `str [url]` `(default: '')`

saucelabs
---------

* **username**: Saucelabs username `str` `(default: '')`

* **key**: Saucelabs key `str` `(default: '')`

proxy_driver
------------

* **use_javascript_dnd**: Use javascript to perform drag and drop. If set to false then the ActionChains.drag_and_drop with be used instead. `bool` `(default: false)`

* **wait_until_visible_before_find**: If this options is set to true then each time you use the driver.find(selector) the proxy_driver will wait until the element is visible; if the element is not visible before the given timeout then it may wait_until_present(selector), raise an exception or return false. All of this is configurable from the brome.yml or provided to the function find(selector, wait_until_visible = (False | True)) directly via kwargs. `bool` `(default: false)`

* **intercept_javascript_error**: If set to true this options will execute some javascript code on each driver.get() that will intercept javascript error. `bool` `(default: false)`

* **validate_xpath_selector**: If set to true the proxy driver will raise an exception if the provided xpath selector is invalid. `bool` `(default: false)`

* **validate_css_selector**: If set to true the proxy driver will raise an exception if the provided css selector is invalid. `bool` `(default: false)`

* **default_timeout**: The default timeout in second. This will be used in a lot of the proxy driver function (wait_until_*); you can overwrite this default with the timeout kwargs. `int (second)` `(default: 5)`

* **raise_exception**: This options tell the brome driver to raise exception on failure (find_*, wait_until_*) or just return a bool instead. `bool` `(default: true)`

* **wait_until_present_before_assert_present**: Wait until not present before assert present. `bool` `(default: false)`

* **wait_until_not_present_before_assert_not_present**: Wait until not present  before assert not present. `bool` `(default: false)`

* **wait_until_not_visible_before_assert_not_visible**: Wait until not visible before assert not visible. `bool` `(default: false)`

* **wait_until_visible_before_assert_visible**: Wait until visible before assert visible. `bool` `(default: false)`

* **wait_until_present_before_find**: Wait until visible before find. `bool` `(default: false)`

* **take_screenshot_on_assertion_success**: Take screenshot on assertion success `bool` `(default: false)`

* **take_screenshot_on_assertion_failure**: Take screenshot on assertion failure `bool` `(default: false)`

proxy_element
-------------

* **use_touch_instead_of_click**: Use touch instead of click. `bool` `(default: false)`

browser
-------

* **window_x_position**: Window x position. `int` `(default: 0)`

* **window_y_position**: Window y position. `int` `(default: 0)`

* **window_height**: Window height. `int` `(default: 725)`

* **window_width**: Window width. `int` `(default: 1650)`

* **maximize_window**: Maximize window. `Note: this may not work in a xvfb environment; so set the width and height manually in this case.` `bool` `(default: false)`

highlight
---------

* **highlight_on_assertion_success**: Highlight on assertion success. `bool` `(default: false)`

* **highlight_on_assertion_failure**: Highlight on assertion failure. `bool` `(default: false)`

* **highlight_when_element_is_clicked**: Highlight when element is clicked. `bool` `(default: false)`

* **highlight_when_element_receive_keys**: Highlight when element received keys. `bool` `(default: false)`

* **highlight_when_element_is_visible**: Highlight when element is visible. `bool` `(default: false)`

* **style_when_element_is_clicked**: Style when element is clicked. `str` `'background: yellow; border: 2px solid red;'`

* **style_when_element_receive_keys**: Style when element receive keys. `str` `'background: yellow; border: 2px solid red;'`

* **style_on_assertion_failure**: Style on assertion failure. `str` `'background: red; border: 2px solid black;'`

* **style_on_assertion_success**: Style on assertion success. `str` `'background: green; border: 2px solid black;'`

* **style_when_element_is_visible**: Style when element is visible. `str` `'background: purple; border: 2px solid black;'`

* **use_highlight**: Use highlight. `bool` `(default: false)`

runner
------

* **embed_on_assertion_success**: Embed on assertion success. `bool` `(default: false)`

* **embed_on_assertion_failure**: Embed on assertion failure. `bool` `(default: false)`

* **embed_on_test_crash**: Embed on test crash. `bool` `(default: false)`

* **play_sound_on_test_crash**: Play sound on test crash. `bool` `(default: false)`

* **play_sound_on_assertion_success**: Play sound on assertion success. `bool` `(default: false)`

* **play_sound_on_assertion_failure**: Play sound on assertion failure. `bool` `(default: false)`

* **play_sound_on_test_finished**: Play sound on test batch finished. `bool` `(default: false)`

* **play_sound_on_ipython_embed**: Play sound on ipython embed. `bool` `(default: false)`

* **play_sound_on_pdb**: Play sound on pdb. `bool` `(default: false)`

* **sound_on_test_crash**: Sound on test crash. `str` `Crash`

* **sound_on_assertion_success**: sound on assertion success. `str` `{testid} succeeded`

* **sound_on_assertion_failure**: Sound on assertion failure. `str` `{testid} failed`

* **sound_on_test_finished**: Sound on test batch finished. `str` `Test finished`

* **sound_on_ipython_embed**: Sound on ipython embed. `str` `Attention required`

* **sound_on_pdb**: Sound on pdb. `str` `Attention required`

* **cache_screenshot**: Use the cache screenshot. `bool` `(default: true)`

database
--------

* **sqlalchemy.url**: the database url `str` `(default: '')`

logger_runner
-------------

* **level**: `'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'` `(default: INFO)`

* **streamlogger**: The logger with output to the sdtout. `bool` `(default: true)`

* **filelogger**: The logger with output to a file in the test batch result directory. `bool` `(default: true)`

* **format**: Logger format. `str` `(default: [%(batchid)s]%(message)s)`

logger_test
-----------

* **level**: `'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'` `(default: INFO)`

* **streamlogger**: The logger with output to the sdtout. `bool` `(default: true)`

* **filelogger**: The logger with output to a file in the test batch result directory. `bool` `(default: true)`

* **format**: Logger format. `str` `(default: [%(batchid)s](%(testname)s):%(message)s)`

ec2
----

* **wait_after_instance_launched**: Wait X seconds after the instances are launched. `int [second]` `(default: 30)`

* **wait_until_system_and_instance_check_performed**: Wait until system and instance checks are performed. `bool` `(default: true)`

grid_runner
-----------

* **max_running_time**: This is the time limit the grid runner can run before raising a TimeoutException. This is to prevent a test batch from running forever using up precious resources. `(int [second])` `(default: 7200)`

* **start_selenium_server**: Start selenium server automatically. `bool` `(default: true)`

* **selenium_server_ip**: Selenium server ip address. `str` `(default: 'localhost')`

* **selenium_server_port**: Selenium port. `int` `(default: 4444)`

* **selenium_server_command**: Selenium server command. `str` `(default: '')`

* **selenium_server_jar_path**: Selenium server jar path. `str [path]` `(default: '')`

* **selenium_hub_config**: Selenium server hub config path. `str [path]` `(default: '')`

* **kill_selenium_server**: Kill selenium server when the test batch finished. `bool` `(default: true)`

webserver
---------

* **open_browser**: Open the webserver index in a new tab on start. `bool` `(default: false)`

* **level**: `'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'` `(default: INFO)`

* **streamlogger**: The logger with output to the sdtout. `bool` `(default: true)`

* **filelogger**: The logger with output to a file in the test batch result directory. `bool` `(default: true)`

* **CLOSED_REGISTRATION**: This options will required the user to enter a token if he want to register in the brome webserver. `bool` `(default: false)`

* **REGISTRATION_TOKEN**: The token used to register in the brome webserver. `str` `(default: '')`

* **HOST**: [FLASK CONFIG]

* **PORT**: [FLASK CONFIG]

* **DEBUG**: [FLASK CONFIG]

* **CACHE_TYPE**: [FLASK CONFIG]

* **ASSETS_DEBUG**: [FLASK CONFIG]

* **DEBUG_TB_INTERCEPT_REDIRECTS**: [FLASK CONFIG]

* **DEBUG_TB_ENABLED**: [FLASK CONFIG]

* **SECRET_KEY**: [FLASK CONFIG]
