from brome import config

def selector_function_resolver(selector):
    selector_type = selector[0:2]
    effective_selector = selector

    if selector_type == 'nm':
        func = 'find_elements_by_name'

    elif selector_type == 'xp':
        func = 'find_elements_by_xpath'

    elif selector_type == 'cn':
        func = 'find_elements_by_class_name'

    elif selector_type == 'id':
        func = 'find_element_by_id'

    elif selector_type == 'cs':
        func = 'find_elements_by_css_selector'

    elif selector_type == 'tn':
        func = 'find_elements_by_tag_name'

    elif selector_type == 'lt':
        func = 'find_elements_by_link_text'

    elif selector_type == 'pl':
        func = 'find_elements_by_partial_link_text'

    elif selector_type == 'sv':
        return selector_function_resolver(config['selector_variable_dict'][selector[3:]])

    else:
        raise Exception("""
            Cannot resolve selector function name! All selector need to start with either:
                'nm:' (name), 'xp:' (xpath), 'cn:' (classname), 'id:' (id), 'cs:' (css), 'tn:' (tag name), 'lt:' (link text), 'pl:' (partial link text)
        """)

    print 'func', func
    print 'effective_selector', effective_selector
    return func, effective_selector
