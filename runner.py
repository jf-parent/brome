#!/usr/bin/env python

from brome.core.models.utils import *
from selenium import webdriver
from IPython import embed
from selenium.webdriver.common.keys import Keys
from brome.core.models.proxy_driver import ProxyDriver

try:
    driver = webdriver.Firefox()
    pdriver = ProxyDriver(driver)
    pdriver.get("http://www.python.org")
    pdriver.find("tn:a")
    embed()
except:
    raise
finally:
    pdriver.close()
