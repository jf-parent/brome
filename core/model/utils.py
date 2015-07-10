#! -*- coding: utf-8 -*-

from urlparse import urlparse
import string
import os
from pudb import set_trace
import traceback
from datetime import datetime
import sys
from subprocess import call
from selenium.common.exceptions import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython import embed

def get_timestamp():
    return datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def string_to_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_')
    return filename

def say(msg):
    if sys.platform in ['win32', 'linux2']:
        call(["espeak", msg])
    else:
        call(["say", msg])

def create_dir_if_doesnt_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
