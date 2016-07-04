default_config = {}

# BROWSER
default_config["browser"] = {}
default_config["browser"]["maximize_window"]= False
default_config["browser"]["window_height"]= 725
default_config["browser"]["window_width"]= 1650
default_config["browser"]["window_x_position"]= 0
default_config["browser"]["window_y_position"]= 0

# DATABASE
default_config["database"] = {}
default_config["database"]["mongo_database_name"]= 'cob_v1_test'

# EC2
default_config["ec2"] = {}
default_config["ec2"]["wait_after_instance_launched"]= 30
default_config["ec2"]["wait_until_system_and_instance_check_performed"]= True

# GRID RUNNER
default_config["grid_runner"] = {}
default_config["grid_runner"]["kill_selenium_server"]= True
default_config["grid_runner"]["max_running_time"]= 7200
default_config["grid_runner"]["selenium_hub_default_config"]= '/Users/pyrat/Documents/PROG/PYTHON/cob_v1/resources/hub-default_config.json'
default_config["grid_runner"]["selenium_server_command"]= 'java -jar {selenium_server_jar_path} -role hub -hubdefault_config {selenium_hub_default_config} -DPOOL_MAX 512 &'
default_config["grid_runner"]["selenium_server_ip"]= 'localhost'
default_config["grid_runner"]["selenium_server_jar_path"]= '/Users/pyrat/Documents/PROG/PYTHON/cob_v1/resources/selenium-server-standalone.jar'
default_config["grid_runner"]["selenium_server_port"]= 4444
default_config["grid_runner"]["start_selenium_server"]= True

# HIGHLIGHT
default_config["highlight"] = {}
default_config["highlight"]["highlight_on_assertion_failure"]= True
default_config["highlight"]["highlight_on_assertion_success"]= True
default_config["highlight"]["highlight_when_element_is_clicked"]= True
default_config["highlight"]["highlight_when_element_is_visible"]= True
default_config["highlight"]["highlight_when_element_receive_keys"]= True
default_config["highlight"]["style_on_assertion_failure"]= 'background: red; border: 2px solid black;'
default_config["highlight"]["style_on_assertion_success"]= 'background: green; border: 2px solid black;'
default_config["highlight"]["style_when_element_is_clicked"]= 'background: yellow; border: 2px solid red;'
default_config["highlight"]["style_when_element_is_visible"]= 'background: purple; border: 2px solid black;'
default_config["highlight"]["style_when_element_receive_keys"]= 'background: yellow; border: 2px solid red;'
default_config["highlight"]["use_highlight"]= True

# LOGGER RUNNER
default_config["logger_runner"] = {}
default_config["logger_runner"]["filelogger"]= True
default_config["logger_runner"]["format"]= "[%(batchid)s]\e[32m%(message)s\e[0m"
default_config["logger_runner"]["level"]= 'INFO'
default_config["logger_runner"]["streamlogger"]= True

# LOGGER TEST
default_config["logger_test"] = {}
default_config["logger_test"]["filelogger"]= True
default_config["logger_test"]["format"]= "[%(batchid)s]\e[34m(%(testname)s)\e[0m:\e[32m%(message)s\e\[0m"
default_config["logger_test"]["level"]= 'INFO'
default_config["logger_test"]["streamlogger"]= True

# PROJECT
default_config["project"] = {}
default_config["project"]["gather_javascript_error"]= True
default_config["project"]["test_batch_result_path"]= False

# PROXY DRIVER
default_config["proxy_driver"] = {}
default_config["proxy_driver"]["default_timeout"]= 5
default_config["proxy_driver"]["intercept_javascript_error"]= True
default_config["proxy_driver"]["raise_exception"]= True
default_config["proxy_driver"]["take_screenshot_on_assertion_failure"]= True
default_config["proxy_driver"]["take_screenshot_on_assertion_success"]= False
default_config["proxy_driver"]["validate_css_selector"]= True
default_config["proxy_driver"]["validate_xpath_selector"]= True
default_config["proxy_driver"]["wait_until_not_present_before_assert_not_present"]= True
default_config["proxy_driver"]["wait_until_not_visible_before_assert_not_visible"]= True
default_config["proxy_driver"]["wait_until_present_before_assert_present"]= True
default_config["proxy_driver"]["wait_until_present_before_find"]= True
default_config["proxy_driver"]["wait_until_visible_before_assert_visible"]= True
default_config["proxy_driver"]["wait_until_visible_before_find"]= True

# RUNNER
default_config["runner"] = {}
default_config["runner"]["cache_screenshot"]= True
default_config["runner"]["embed_on_assertion_failure"]= True
default_config["runner"]["embed_on_assertion_success"]= False
default_config["runner"]["embed_on_test_crash"]= True
default_config["runner"]["play_sound_on_assertion_failure"]= True
default_config["runner"]["play_sound_on_assertion_success"]= False
default_config["runner"]["play_sound_on_ipython_embed"]= True
default_config["runner"]["play_sound_on_pdb"]= True
default_config["runner"]["play_sound_on_test_crash"]= True
default_config["runner"]["play_sound_on_test_finished"]= True
default_config["runner"]["sound_on_assertion_failure"]= '{testid} failed'
default_config["runner"]["sound_on_assertion_success"]= '{testid} succeeded'
default_config["runner"]["sound_on_ipython_embed"]= 'Attention required'
default_config["runner"]["sound_on_pdb"]= 'Attention required'
default_config["runner"]["sound_on_test_crash"]= 'Crash'
default_config["runner"]["sound_on_test_finished"]= 'Test finished'
