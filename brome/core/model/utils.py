#! -*- coding: utf-8 -*-

from urlparse import urlparse
import string
import os
import traceback
from datetime import datetime
import sys
from subprocess import call, Popen
from time import sleep

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython import embed
from pudb import set_trace
import psutil

from .exceptions import *

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def string_to_filename(s):
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
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

if sys.platform == 'win32':
    devnull = open('log-null', 'w')
else:
    devnull = open('/dev/null', 'w')

def kill_by_pid(pid):
    p = psutil.Process(pid)
    p.terminate()
    print '[pid:%s]killed'%pid

def kill_by_name(procname):
    for proc in psutil.process_iter():
        if proc.name() == procname:
            print '[pid:%s][name:%s] killed'%(proc.pid, proc.name())
            proc.kill()

def kill_by_found_string_in_cmdline(procname, string):
    for proc in psutil.process_iter():
        if proc.name() == procname:
            for cmd in proc.cmdline():
                if cmd.find(string) != -1:
                    print '[pid:%s][name:%s] killed'%(proc.pid, proc.name())
                    proc.kill()
