
from pudb import set_trace
import traceback
import sys
from subprocess import call
from selenium.common.exceptions import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython import embed

def say(msg):
    if sys.platform in ['win32', 'linux2']:
        call(["espeak", msg])
    else:
        call(["say", msg])
