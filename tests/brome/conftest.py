from threading import Thread
from wsgiref.simple_server import make_server

import selenium
import pytest

from brome import Brome
from brome.runner import ec2_instance
from test_server.server import app
from brome_config import default_config
from brome.core.utils import delete_database
from mock.dummy_ec2_instance import DummyEC2Instance


class DummyWebdriverInstance(object):
    def __init__(self):
        self.capabilities = {
            'browserName': 'dummy',
            'platform': 'dummy',
            'version': '1.0.0'
        }

    def __getattr__(self, funcname):
        return lambda *args, **kwargs: None


class WSGIAppServerThread(Thread):

    def run(self):
        make_server('localhost', 1771, app).serve_forever()


def pytest_sessionstart(session):
    app = WSGIAppServerThread()
    app.daemon = True
    app.start()

    delete_database(
        default_config['database']['mongo_database_name'],
        flush_redis=False
    )


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name",
        action="store",
        default="phantomjs",
        help="Browser name: phantomjs, firefox or chrome"
    )


@pytest.fixture(scope="module")
def browser_name(request):
    return request.config.getoption("--browser-name")


@pytest.fixture(scope="function")
def selenium_monkeypath(monkeypatch):
    def Remote(*args, **kwargs):
        return DummyWebdriverInstance()

    monkeypatch.setattr(selenium.webdriver, 'Remote', Remote)


@pytest.fixture(scope="function")
def ec2_instance_monkeypath(monkeypatch):
    monkeypatch.setattr(
        ec2_instance,
        'EC2Instance',
        DummyEC2Instance
    )


@pytest.fixture
def brome():
    brome = Brome(
        config=default_config
    )
    return brome
