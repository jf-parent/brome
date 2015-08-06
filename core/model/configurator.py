#! -*- coding: utf-8 -*-

import ConfigParser

def get_config_value(dict_list, config_name):
    try:
        section, option = config_name.split(':')
    except ValueError:
        raise Exception("""
            [get_config_value] config_name should contains the section 
            and the options separated by a colon (eg runner:tests_config)
        """)

    for dict_ in dict_list:
        if dict_.has_key(section):
            if option == '*':
                return dict_[section]
            if dict_[section].has_key(option):
                if type(dict_[section][option]) is dict:
                    return dict_[section][option].get('default')
                else:
                    return dict_[section][option]

def test_config_to_dict(test_config_string):
    test_config = {}
    if test_config_string:
        for config in test_config_string.split(','):
            key, value = config.split('=')
            test_config[key] = value

    return test_config

def ini_to_dict(ini_path):
    config = {}

    config_parser = ConfigParser.SafeConfigParser()

    config_parser.read(ini_path)

    for section in config_parser.sections():
        config[section] = {}
        for option in config_parser.options(section):
            value = config_parser.get(section, option)

            if section == 'webserver':
                option = option.upper()

            effective_value = value
            if value.lower() in ['false', 'true']:
                 effective_value = config_parser.getboolean(section, option)
            #NOTE will only work with positive integer;
            #not a problem for now since we only have positive integer
            elif value.isdigit():
                effective_value = config_parser.getint(section, option)

            config[section][option] = effective_value

    return config

def runner_args_to_dict(args):
    config = {}

    brome_config_string = args.brome_config
    if brome_config_string:

        for config_str in brome_config_string.split(','):
            section, option = config_str.split(':')
            option, value = option.split('=')

            if not config.has_key(section):
                config[section] = {}

            effective_value = value
            #NOTE will only work with positive integer;
            #not a problem for now since we only have positive integer
            if value.isdigit():
                effective_value = int(value)
            elif value.lower() in ['false', 'true']:
                if value.lower() == 'false':
                    effective_value = False
                else:
                    effective_value = True

            config[section][option] = effective_value

    config['runner'] = {}
    for arg, value in args.__dict__.iteritems():
        config['runner'][arg] = value

    return config

def parse_brome_config_from_browser_config(browser_config):
    config = {}

    brome_keys = [key for key in browser_config.iterkeys() if key.find(':') != -1]

    for brome_key in brome_keys:
        section, option = brome_key.split(':')
        value = browser_config[brome_key]

        if not config.has_key(section):
            config[section] = {}

        config[section][option] = value

    return config

default_config = {}

###SECTIONS
default_config["project"] = {}
default_config["proxy_driver"] = {}
default_config["browser"] = {}
default_config["highlight"] = {}
default_config["runner"] = {}
default_config["database"] = {}
default_config["logger_runner"] = {}
default_config["logger_test"] = {}
default_config["ec2"] = {}
default_config["grid_runner"] = {}

#OPTIONS
default_config["grid_runner"]["max_running_time"] = {
    'default': 7200,
    'type': 'number',
    'min': 0,
    'title': 'Max running time'
}

default_config["grid_runner"]["start_selenium_server"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Start selenium server automatically'
}

default_config["grid_runner"]["selenium_server_ip"] = {
    'default': 'localhost',
    'type': 'input',
    'title': 'Selenium server ip address'
}

default_config["grid_runner"]["selenium_server_port"] = {
    'default': 4444,
    'type': 'number',
    'min': 0,
    'title': 'Selenium port'
}
default_config["grid_runner"]["selenium_server_command"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Selenium server command'
}

default_config["grid_runner"]["kill_selenium_server"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Kill selenium server when the test batch finished'
}

default_config["ec2"]['wait_after_instance_launched'] = {
    'default': 30,
    'type': 'number',
    'min': 0,
    'title': 'Wait X seconds after the instances are launched'
}

default_config["ec2"]['wait_until_system_and_instance_check_performed'] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Wait until system and instance checks are performed'
}

default_config["project"]["test_batch_result_path"] = {
    'default': "",
    'type': 'input',
    'title': 'Test batch result path'
}

default_config["logger_runner"]["level"] = {
    'default': "INFO",
    'type': 'dropdown',
    'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'title': 'Logger level'
}

default_config["logger_runner"]["streamlogger"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Use stream logger'
}

default_config["logger_runner"]["filelogger"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Use file logger'
}

default_config["logger_runner"]["format"] = {
    'default': "[%%(batchid)s]%%(message)s",
    'type': 'input',
    'title': 'Logger format'
}

default_config["logger_test"]["level"] = {
    'default': "INFO",
    'type': 'dropdown',
    'options': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'title': 'Logger level'
}

default_config["logger_test"]["streamlogger"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Use stream logger'
}

default_config["logger_test"]["filelogger"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Use file logger'
}

default_config["logger_test"]["format"] = {
    'default': "[%%(batchid)s](%%(testname)s):%%(message)s",
    'type': 'input',
    'title': 'Logger format'
}

default_config["proxy_driver"]["validate_xpath_selector"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Validate xpath selector'
}

default_config["proxy_driver"]["validate_css_selector"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Validate css selector'
}

default_config["proxy_driver"]["default_timeout"] = {
    'default': 5,
    'type': 'number',
    'min': 0,
    'title': 'Default timeout'
}

default_config["proxy_driver"]["raise_exception"] = {
    'default': True,
    'type': 'checkbox',
    'title': 'Raise exception'
}

default_config["proxy_driver"]["wait_until_visible_before_find"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Wait until visible before find'
}

default_config["proxy_driver"]["take_screenshot_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Take screenshot on assertion success'
}

default_config["proxy_driver"]["take_screenshot_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Take screenshot on assertion failure'
}

default_config["browser"]["window_x_position"] = {
    'default': 0,
    'type': 'number',
    'min': 0,
    'title': 'Window x position'
}

default_config["browser"]["window_y_position"] = {
    'default': 0,
    'type': 'number',
    'min': 0,
    'title': 'Window y position'
}

default_config["browser"]["window_height"] = {
    'default': 725,
    'type': 'number',
    'min': 0,
    'title': 'Window height'
}

default_config["browser"]["window_width"] = {
    'default': 1650,
    'type': 'number',
    'min': 0,
    'title': 'Window width'
}

default_config["browser"]["maximize_window"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Maximize window'
}

default_config["highlight"]["element_is_clicked"] = {
    'default': "background: yellow; border: 2px solid red;",
    'type': 'input',
    'title': 'Element is clicked'
}

default_config["highlight"]["element_receive_keys"] = {
    'default': "background: yellow; border: 2px solid red;",
    'type': 'input',
    'title': 'Element receive keys'
}

default_config["highlight"]["on_assertion_failure"] = {
    'default': "background: red; border: 2px solid black;",
    'type': 'input',
    'title': 'On assertion failure'
}

default_config["highlight"]["on_assertion_success"] = {
    'default': "background: green; border: 2px solid black;",
    'type': 'input',
    'title': 'On assertion success style'
}

default_config["highlight"]["element_is_visible"] = {
    'default': "background: purple; border: 2px solid black;",
    'type': 'input',
    'title': 'Element is visible style'
}

default_config["highlight"]["use_highlight"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Use highlight'
}

default_config["runner"]["embed_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Embed on assertion success'
}

default_config["runner"]["embed_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Embed on assertion failure'
}

default_config["runner"]["embed_on_test_crash"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Embed on test crash'
}

default_config["runner"]["play_sound_on_test_crash"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on test crash'
}

default_config["runner"]["play_sound_on_assertion_success"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on assertion success'
}

default_config["runner"]["play_sound_on_assertion_failure"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on assertion failure'
}

default_config["runner"]["play_sound_on_test_finished"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on test batch finished'
}

default_config["runner"]["play_sound_on_ipython_embed"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on ipython embed'
}

default_config["runner"]["play_sound_on_pdb"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Play sound on pdb'
}

default_config["runner"]["sound_on_test_crash"] = {
    'default': 'Crash',
    'type': 'input',
    'title': 'Sound on test crash'
}

default_config["runner"]["sound_on_assertion_success"] = {
    'default': "{testid} succeeded",
    'type': 'input',
    'title': 'sound on assertion success'
}

default_config["runner"]["sound_on_assertion_failure"] = {
    'default': "{testid} failed",
    'type': 'input',
    'title': 'Sound on assertion failure'
}

default_config["runner"]["sound_on_test_finished"] = {
    'default': "Test finished",
    'type': 'input',
    'title': 'Sound on test batch finished'
}

default_config["runner"]["sound_on_ipython_embed"] = {
    'default': "Attention required",
    'type': 'input',
    'title': 'Sound on ipython embed'
}

default_config["runner"]["sound_on_pdb"] = {
    'default': "Attention required",
    'type': 'input',
    'title': 'Sound on pdb'
}

default_config["runner"]["cache_screenshot"] = {
    'default': False,
    'type': 'checkbox',
    'title': 'Use the cache screenshot'
}

default_config["database"]["sqlalchemy.url"] = {
    'default': "",
    'type': 'input',
    'title': 'Sqlalchemy url'
}
