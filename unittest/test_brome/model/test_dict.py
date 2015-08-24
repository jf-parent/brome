test_dict = {}
test_dict['#1'] = "Finding element with wait until visible should return that element if that element become visible before the timeout is reached"
test_dict['#2'] = "Finding element with wait until visible should return None if that element is not visible."
test_dict['#3'] = "Finding element with waiting until visible should raise Timeout exception if that element is not visible and raise_exception is set to True."
test_dict['#4'] = "get_javascript_error return_type list return [] when there is not javascript error."
test_dict['#5'] = "get_javascript_error return_type string return $no_javascript_error_string when there is not javascript error."
test_dict['#6'] = "get_javascript_error return_type list return [js_error1, js_error2] when there is javascript error."
test_dict['#7'] = "get_javascript_error return_type string return '<rc>'.join(js_error_list) when there is javascript error."
