from threading import Thread
from wsgiref.simple_server import make_server

import pytest

from brome import Brome
from test_server.server import app
from brome_config import default_config
from brome.core.utils import delete_database


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


@pytest.fixture
def brome():
    brome = Brome(
        config=default_config
    )
    return brome
