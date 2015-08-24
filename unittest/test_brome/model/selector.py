selector_dict = {}
selector_dict['example_find_by_tag_name'] = "tn:a"
selector_dict['example_find_by_id'] = "id:1"
selector_dict['example_find_by_xpath'] = "xp://*[@class = 'xpath']"
selector_dict['example_find_by_partial_link_text'] = "pl:partial link text"
selector_dict['example_find_by_link_text'] = "lt:link text"
selector_dict['example_find_by_css_selector'] = "cs:.classname"
selector_dict['example_find_by_classname'] = "cn:classname"
selector_dict['example_find_by_name'] = "nm:name"
selector_dict['example_multiple_selector'] = {
    "default" : "xp://*[contains(@class, 'default')]",
    "chrome|iphone|android" : "xp://*[contains(@class, 'special')]"
}
