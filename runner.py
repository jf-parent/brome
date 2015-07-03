#!/usr/bin/env python

from selenium import webdriver
from IPython import embed
from selenium.webdriver.common.keys import Keys
from brome.core.models.proxy_driver import ProxyDriver

try:
    driver = webdriver.Firefox()
    pdriver = ProxyDriver(driver)
    pdriver.get("http://www.python.org")
    """
    elem = pdriver.get_first("nm:q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    """

    """
    elements = pdriver.get_all("tn:a")
    for element in elements:
        element.click()
    """

    """
    element = pdriver.get_first("sv:download_btn")
    element.click()
    """

    elements = pdriver.get_all("tn:a")
    elements = elements[2:4]
    for element in elements:
        element.click()
    
    embed()
except:
    raise
finally:
    pdriver.close()
