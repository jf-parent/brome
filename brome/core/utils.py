import string
import os
from datetime import datetime
import sys
from subprocess import call

from redis import StrictRedis
from contextlib import ContextDecorator
from mongoalchemy.session import Session
from pymongo import MongoClient

import psutil


class DbSessionContext(ContextDecorator):
    def __init__(self, mongo_database_name):
        self.session = Session.connect(
            mongo_database_name
        )

    def __enter__(self):
        return self.session

    def __exit__(self, *exc):
        self.session.end()
        self.session.db.client.close()
        return False


def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def string_to_filename(s):
    valid_chars = "-_. %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')
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
    print('[pid:%s]killed' % pid)


def kill_by_name(procname):
    for proc in psutil.process_iter():
        if proc.name() == procname:
            print('[pid:%s][name:%s] killed' % (proc.pid, proc.name()))
            proc.kill()


def kill_by_found_string_in_cmdline(procname, string):
    for proc in psutil.process_iter():
        if proc.name() == procname:
            for cmd in proc.cmdline():
                if cmd.find(string) != -1:
                    print('[pid:%s][name:%s] killed' % (proc.pid, proc.name()))
                    proc.kill()


def delete_database(db_name, flush_redis=True):
    mongo_client = MongoClient()
    mongo_client.drop_database(db_name)
    print('Database (%s) deleted!' % db_name)

    if flush_redis:
        redis_client = StrictRedis()
        redis_client.flushall()
        print('Redis flushed all')


def update_test(session, test_dict):
    from brome.model.test import Test
    print('Updating the test')
    for test_id, test_config in iter(test_dict.items()):
        if type(test_config) == dict:
            name = test_config['name']
        else:
            name = test_config

        # NEW TEST
        if not session.query(Test).filter(Test.test_id == test_id).count():
            test = Test(test_id=test_id, name=name)
            print('Added test id', test_id)
        # UPDATE TEST
        else:
            test = session.query(Test).filter(Test.test_id == test_id).one()
            if test.name != name:
                test.name = name
                print('Updated test id', test_id)

        session.save(test, safe=True)

    print('Done!')
