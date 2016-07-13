#! /usr/bin/env python

from IPython import embed
from mongoalchemy.session import Session

from brome.webserver.server.settings import config
from brome.model.user import User  # noqa
from brome.model.notification import Notification  # noqa
from brome.model.testbatch import Testbatch  # noqa
from brome.model.testcrash import Testcrash  # noqa
from brome.model.testresult import Testresult  # noqa
from brome.model.test import Test  # noqa
from brome.model.testinstance import Testinstance  # noqa

config.configure()

session = Session.connect(config.get("MONGO_DATABASE_NAME"))

embed()
