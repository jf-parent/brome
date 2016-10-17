def generate_brome_config():
    """Generate a brome config with default value

    Returns:
        config (dict)
    """

    config = {}
    for key in iter(default_config):
        for inner_key, value in iter(default_config[key].items()):
            if key not in config:
                config[key] = {}

            config[key][inner_key] = value['default']

    return config


def test_config_to_dict(test_config_string):
    """Parse the test config to a dictionary

    Args:
        test_config_string (str) this string come from the --test-config
        flag of the bro executable run command
    """

    test_config = {}
    if test_config_string:
        for config in test_config_string.split(','):
            key, value = config.split('=')
            test_config[key] = value

    return test_config


def parse_brome_config_from_browser_config(browser_config):
    """Parse the browser config and look for brome specific config

    Args:
        browser_config (dict)
    """

    config = {}

    brome_keys = [key for key in browser_config if key.find(':') != -1]

    for brome_key in brome_keys:
        section, option = brome_key.split(':')
        value = browser_config[brome_key]

        if section not in config:
            config[section] = {}

        config[section][option] = value

    return config

default_config = {}

# ##SECTIONS
default_config["mitmproxy"] = {}
default_config["brome"] = {}
default_config["project"] = {}
default_config["saucelabs"] = {}
default_config["browserstack"] = {}
default_config["proxy_driver"] = {}
default_config["proxy_element"] = {}
default_config["browser"] = {}
default_config["highlight"] = {}
default_config["runner"] = {}
default_config["database"] = {}
default_config["logger_runner"] = {}
default_config["bot_diary"] = {}
default_config["logger_test"] = {}
default_config["ec2"] = {}
default_config["grid_runner"] = {}
default_config["webserver"] = {}
default_config["runner_args"] = {}

# RUNNER ARGS
default_config["runner_args"]["remote_runner"] = {
    'default': '',
    'type': 'input',
    'visible': False,
    'title': ''
}

default_config["runner_args"]["localhost_runner"] = {
    'default': '',
    'type': 'input',
    'visible': False,
    'title': ''
}

# MITMPROXY
default_config["mitmproxy"]["path"] = {
    'default': '',
    'type': 'input',
    'visible': False,
    'title': 'The path to the mitmproxy python bin'
}

default_config["mitmproxy"]["filter"] = {
    'default': '',
    'type': 'input',
    'visible': False,
    'title': 'The mitmproxy filter'
}

# BROME
default_config["brome"]["script_folder_name"] = {
    'default': 'tests',
    'type': 'input',
    'visible': False,
    'title': 'The name of the folder holding the scripts'
}

default_config["brome"]["script_test_prefix"] = {
    'default': 'test_',
    'type': 'input',
    'visible': False,
    'title': 'The prefix of the script'
}

default_config["brome"]["brome_executable_name"] = {
    'default': 'bro',
    'type': 'input',
    'visible': False,
    'title': 'The brome executable name'
}

# PROXY ELEMENT
default_config["proxy_element"]["use_touch_instead_of_click"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use touch instead of click'
}

default_config["proxy_element"]["wait_until_clickable"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until clickable'
}

# BROWSERSTACK
default_config["browserstack"]["username"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'Browserstack username'
}

default_config["browserstack"]["key"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'Browserstack key'
}

# SAUCELABS
default_config["saucelabs"]["username"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'Saucelabs username'
}

default_config["saucelabs"]["key"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'Saucelabs key'
}

# GRID RUNNER
default_config["grid_runner"]["max_running_time"] = {
    'default': 7200,
    'type': 'number',
    'visible': True,
    'title': 'Max running time'
}

default_config["grid_runner"]["start_selenium_server"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Start selenium server automatically'
}

default_config["grid_runner"]["selenium_server_ip"] = {
    'default': 'localhost',
    'type': 'input',
    'visible': True,
    'title': 'Selenium server ip address'
}

default_config["grid_runner"]["selenium_server_port"] = {
    'default': 4444,
    'type': 'number',
    'visible': True,
    'title': 'Selenium port'
}
default_config["grid_runner"]["selenium_server_command"] = {
    'default': "",
    'type': 'input',
    'visible': True,
    'title': 'Selenium server command'
}

default_config["grid_runner"]["selenium_server_jar_path"] = {
    'default': "",
    'type': 'input',
    'visible': True,
    'title': 'Selenium server jar path'
}

default_config["grid_runner"]["selenium_hub_config"] = {
    'default': "",
    'type': 'input',
    'visible': True,
    'title': 'Selenium server hub config path'
}

default_config["grid_runner"]["kill_selenium_server"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Kill selenium server when the test batch finished'
}

# EC2
default_config["ec2"]['wait_after_instance_launched'] = {
    'default': 30,
    'type': 'number',
    'visible': True,
    'title': 'Wait X seconds after the instances are launched'
}

default_config["ec2"]['wait_until_system_and_instance_check_performed'] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until system and instance checks are performed'
}

# PROJECT
default_config["project"]["script_folder_name"] = {
    'default': "tests",
    'type': 'input',
    'visible': True,
    'title': 'The script folder name'
}

default_config["project"]["test_batch_result_path"] = {
    'default': "",
    'type': 'input',
    'visible': True,
    'title': 'Test batch result path'
}

default_config["project"]["url"] = {
    'default': "",
    'type': 'input',
    'visible': True,
    'title': 'The url of the server on which the test run (must include the protocol) e.g.:https://the-internet.herokuapp.com/'  # noqa
}

# LOGGER RUNNER
default_config["logger_runner"]["level"] = {
    'default': "INFO",
    'type': 'dropdown',
    'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'visible': True,
    'title': 'Logger level'
}

default_config["logger_runner"]["streamlogger"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use stream logger'
}

default_config["logger_runner"]["filelogger"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use file logger'
}

default_config["logger_runner"]["format"] = {
    'default': "[%(batchid)s]%(message)s",
    'type': 'input',
    'visible': True,
    'title': 'Logger format'
}

# LOGGER TEST
default_config["logger_test"]["level"] = {
    'default': "INFO",
    'type': 'dropdown',
    'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'visible': True,
    'title': 'Logger level'
}

default_config["logger_test"]["streamlogger"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use stream logger'
}

default_config["logger_test"]["filelogger"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use file logger'
}

default_config["logger_test"]["format"] = {
    'default': "[%(batchid)s](%(testname)s):%(message)s",
    'type': 'input',
    'visible': True,
    'title': 'Logger format'
}

# PROXY DRIVER
default_config["proxy_driver"]["use_javascript_dnd"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use javascript to perform drag and drop'
}

default_config["proxy_driver"]["wait_until_visible_before_find"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until visible before find'
}

default_config["proxy_driver"]["intercept_javascript_error"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Intercept javascript error'
}

default_config["proxy_driver"]["validate_xpath_selector"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Validate xpath selector'
}

default_config["proxy_driver"]["validate_css_selector"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Validate css selector'
}

default_config["proxy_driver"]["default_timeout"] = {
    'default': 5,
    'type': 'number',
    'visible': True,
    'title': 'Default timeout'
}

default_config["proxy_driver"]["raise_exception"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Raise exception'
}

default_config["proxy_driver"]["wait_until_present_before_assert_present"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until not present before assert present'
}

default_config["proxy_driver"]["wait_until_not_present_before_assert_not_present"] = {  # noqa
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until not present  before assert not present'
}

default_config["proxy_driver"]["wait_until_not_visible_before_assert_not_visible"] = {  # noqa
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until not visible before assert not visible'
}

default_config["proxy_driver"]["wait_until_visible_before_assert_visible"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until visible before assert visible'
}

default_config["proxy_driver"]["wait_until_present_before_find"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Wait until visible before find'
}

default_config["proxy_driver"]["take_screenshot_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Take screenshot on assertion success'
}

default_config["proxy_driver"]["take_screenshot_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Take screenshot on assertion failure'
}

# BROWSER
default_config["browser"]["window_x_position"] = {
    'default': 0,
    'type': 'number',
    'visible': True,
    'title': 'Window x position'
}

default_config["browser"]["window_y_position"] = {
    'default': 0,
    'type': 'number',
    'visible': True,
    'title': 'Window y position'
}

default_config["browser"]["window_height"] = {
    'default': 725,
    'type': 'number',
    'visible': True,
    'title': 'Window height'
}

default_config["browser"]["window_width"] = {
    'default': 1650,
    'type': 'number',
    'visible': True,
    'title': 'Window width'
}

default_config["browser"]["maximize_window"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Maximize window'
}

# HIGHLIGHT
default_config["highlight"]["highlight_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Highlight on assertion success'
}

default_config["highlight"]["highlight_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Highlight on assertion failure'
}

default_config["highlight"]["highlight_when_element_is_clicked"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Highlight when element is clicked'
}

default_config["highlight"]["highlight_when_element_receive_keys"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Highlight when element received keys'
}

default_config["highlight"]["element_is_visible"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Highlight when element is visible'
}

default_config["highlight"]["style_when_element_is_clicked"] = {
    'default': "background: yellow; border: 2px solid red;",
    'type': 'input',
    'visible': True,
    'title': 'Element is clicked'
}

default_config["highlight"]["style_when_element_receive_keys"] = {
    'default': "background: yellow; border: 2px solid red;",
    'type': 'input',
    'visible': True,
    'title': 'Element receive keys'
}

default_config["highlight"]["style_on_assertion_failure"] = {
    'default': "background: red; border: 2px solid black;",
    'type': 'input',
    'visible': True,
    'title': 'On assertion failure'
}

default_config["highlight"]["style_on_assertion_success"] = {
    'default': "background: green; border: 2px solid black;",
    'type': 'input',
    'visible': True,
    'title': 'On assertion success style'
}

default_config["highlight"]["style_when_element_is_visible"] = {
    'default': "background: purple; border: 2px solid black;",
    'type': 'input',
    'visible': True,
    'title': 'Element is visible style'
}

default_config["highlight"]["use_highlight"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use highlight'
}

# RUNNER
default_config["runner"]["embed_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Embed on assertion success'
}

default_config["runner"]["embed_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Embed on assertion failure'
}

default_config["runner"]["embed_on_test_crash"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Embed on test crash'
}

default_config["runner"]["play_sound_on_test_crash"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on test crash'
}

default_config["runner"]["play_sound_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on assertion success'
}

default_config["runner"]["play_sound_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on assertion failure'
}

default_config["runner"]["play_sound_on_test_finished"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on test batch finished'
}

default_config["runner"]["play_sound_on_ipython_embed"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on ipython embed'
}

default_config["runner"]["play_sound_on_pdb"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Play sound on pdb'
}

default_config["runner"]["sound_on_test_crash"] = {
    'default': 'Crash',
    'type': 'input',
    'visible': True,
    'title': 'Sound on test crash'
}

default_config["runner"]["sound_on_assertion_success"] = {
    'default': "{testid} succeeded",
    'type': 'input',
    'visible': True,
    'title': 'sound on assertion success'
}

default_config["runner"]["sound_on_assertion_failure"] = {
    'default': '{testid} failed',
    'type': 'input',
    'visible': True,
    'title': 'Sound on assertion failure'
}

default_config["runner"]["sound_on_test_finished"] = {
    'default': 'Test finished',
    'type': 'input',
    'visible': True,
    'title': 'Sound on test batch finished'
}

default_config["runner"]["sound_on_ipython_embed"] = {
    'default': 'Attention required',
    'type': 'input',
    'visible': True,
    'title': 'Sound on ipython embed'
}

default_config["runner"]["sound_on_pdb"] = {
    'default': 'Attention required',
    'type': 'input',
    'visible': True,
    'title': 'Sound on pdb'
}

default_config["runner"]["cache_screenshot"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use the cache screenshot'
}

# DATABASE
default_config["database"]["mongo_database_name"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'Mongo database name'
}

# BOT DIARY
default_config["bot_diary"]["enable_auto_bot_diary"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Enable auto bot diary'
}

default_config["bot_diary"]["enable_auto_bot_diary_component_screenshot"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Enable auto bot diary component screenshot'
}

default_config["bot_diary"]["enable_bot_diary"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Enable bot diary'
}

default_config["bot_diary"]["streamlogger"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use stream logger'
}

default_config["bot_diary"]["filelogger"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use file logger'
}

# WEBSERVER
default_config["webserver"]["LOG_LEVEL"] = {
    'default': 'INFO',
    'type': 'dropdown',
    'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'visible': True,
    'title': 'Logger level'
}

default_config["webserver"]["STREAMLOGGER"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use stream logger'
}

default_config["webserver"]["FILELOGGER"] = {
    'default': True,
    'type': 'checkbox',
    'visible': True,
    'title': 'Use file logger'
}

default_config["webserver"]["ENV"] = {
    'default': 'production',
    'type': 'checkbox',
    'visible': True,
    'title': 'Environnemnt for the server: "production", "test", "development"',  # noqa
}

default_config["webserver"]["CLOSED_REGISTRATION"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'closed registration',
}

default_config["webserver"]["REGISTRATION_TOKEN"] = {
    'default': '',
    'type': 'input',
    'visible': True,
    'title': 'registration token',
}

default_config["webserver"]["PORT"] = {
    'default': 5000,
    'type': 'number',
    'visible': True,
    'title': 'webserver port',
}

default_config["webserver"]["SHOW_QUALITY_SCREENSHOT"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Show the quality screenshot in the detail of a test batch',
}

default_config["webserver"]["SHOW_NETWORK_CAPTURE"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Show the network capture in the detail of a test batch',
}

default_config["webserver"]["SHOW_BOT_DIARY"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Show the bot diary in the detail of a test batch',
}

default_config["webserver"]["SHOW_VIDEO_CAPTURE"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Show the video capture in the detail of a test batch',
}

default_config["webserver"]["SHOW_TEST_INSTANCES"] = {
    'default': False,
    'type': 'checkbox',
    'visible': True,
    'title': 'Show the test instance in the detail of a test batch',
}

default_config["webserver"]["HOST"] = {
    'default': 'localhost',
    'type': 'input',
    'visible': True,
    'title': 'webserver ip',
}

default_config["webserver"]["report"] = {
    'default': False,
    'type': 'input',
    'visible': False,
    'title': 'Config for the report system',
}
