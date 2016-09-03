import asyncio
import os
from datetime import datetime
import types

import pytest
from webtest_aiohttp import TestApp

from brome.core.settings import BROME_CONFIG
from brome.webserver.server.app import init
from brome.core.utils import DbSessionContext, delete_database
from brome.model.user import User
from brome.model.testbatch import Testbatch
from brome.model.test import Test
from brome.model.testcrash import Testcrash
from brome.model.testresult import Testresult
from brome.model.testinstance import Testinstance

HERE = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def client():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    config = {
        "env": "test",
        "mongo_database_name": "webbase_test",
        "mongo_host": "127.0.0.1",
        "server_port": 1337,
        "server_host": "localhost"
    }

    delete_database(config.get('mongo_database_name'))

    BROME_CONFIG['webserver'] = {}
    BROME_CONFIG['webserver'].update(config)
    _, _, app = loop.run_until_complete(init(loop))

    with DbSessionContext(config.get('mongo_database_name')) as session:

        # INSERT DUMMY DATA
        # TEST
        for i in range(2):
            test_context = {
                'db_session': session,
                'data': {
                    'name': 'Test %s' % i,
                    'test_id': str(i)
                }
            }
            test = Test()
            loop.run_until_complete(
                test.validate_and_save(test_context)
            )

        # TEST BATCH
        test_batch_context = {
            'db_session': session,
            'data': {
                'pid': 1337,
                'starting_timestamp': datetime.now(),
                'total_tests': 1
            }
        }
        for i in range(2):
            test_batch = Testbatch()
            loop.run_until_complete(
                test_batch.validate_and_save(test_batch_context)
            )

            if i == 0:
                dummy_log_file_path = os.path.join(
                    HERE,
                    'mock',
                    'test_batch_dummy_log.log'
                )
                test_batch.log_file_path = dummy_log_file_path
                session.save(test_batch, safe=True)

            for index in range(2):
                # TEST INSTANCE
                test_instance_context = {
                    'db_session': session,
                    'data': {
                        'starting_timestamp': datetime.now(),
                        'name': 'Test Instance {index}'.format(index=index),
                        'test_batch_id': test_batch.mongo_id
                    }
                }
                test_instance = Testinstance()
                loop.run_until_complete(
                    test_instance.validate_and_save(test_instance_context)
                )

            # TEST RESULT
            for j in range(5):
                test_result_context = {
                    'db_session': session,
                    'data': {
                        'result': bool(j),
                        'browser_id': 'firefox',
                        'title': 'Test result %s' % i,
                        'test_id': test.mongo_id,
                        'test_instance_id': test_instance.mongo_id,
                        'test_batch_id': test_batch.mongo_id
                    }
                }
                test_result = Testresult()
                loop.run_until_complete(
                    test_result.validate_and_save(test_result_context)
                )

            # TEST CRASH
            test_crash_context = {
                'db_session': session,
                'data': {
                    'browser_id': 'firefox',
                    'title': 'Test Crash',
                    'test_instance_id': test_instance.mongo_id,
                    'test_batch_id': test_batch.mongo_id
                }
            }
            test_crash = Testcrash()
            loop.run_until_complete(
                test_crash.validate_and_save(test_crash_context)
            )

        users = [
            {
                'name': 'test',
                'email': 'test@test.com',
                'password': '123456'
            }, {
                'name': 'to.disable',
                'email': 'to.disable@to.disable.com',
                'password': '123456'
            }, {
                'name': 'admin',
                'email': 'admin@admin.com',
                'password': '123456',
                'role': 'admin'
            }, {
                'name': 'disabled',
                'email': 'disabled@disabled.com',
                'password': '123456',
                'enable': False
            }
        ]

        for user_data in users:
            user = User()
            context = {
                'db_session': session,
                'method': 'create',
                'data': user_data
            }

            loop.run_until_complete(user.validate_and_save(context))

    def login(self, email, password='123456'):
        self.post_json(
            '/api/login',
            {
                'email': email,
                'password': password,
                'token': self.__token__
            }
        )
        with DbSessionContext(
            self.config.get('mongo_database_name')
        ) as session:
            user = session.query(User)\
                .filter(User.email == email).one()

        return user

    client = TestApp(app)
    client.config = config
    client.login = types.MethodType(login, client)

    # NOTE Always do an /api/get_session to init the session correctly
    response = client.get('/api/get_session')
    client.__token__ = response.json['token']

    return client
