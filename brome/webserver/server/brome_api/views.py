import importlib
from glob import glob
import logging
import os
import sys
import tempfile
import subprocess

import yaml
from aiohttp_session import get_session
from aiohttp import web

from brome.core.settings import BROME_CONFIG
from brome.core import exceptions
from brome.webserver.server.server_decorator import (
    require,
    exception_handler
)

logger = logging.getLogger('bromewebserver')


def get_tests():
    test_list = []
    script_test_prefix = BROME_CONFIG['brome']['script_test_prefix']

    tests_dir = os.path.join(
        BROME_CONFIG['project']['absolute_path'],
        BROME_CONFIG['brome']['script_folder_name']
    )

    if os.path.isdir(tests_dir):
        tests = glob(
            os.path.join(tests_dir, '%s*.py' % script_test_prefix)
        )
        for test in sorted(tests):
            name = test.split(os.sep)[-1][len(script_test_prefix):-3]
            test_list.append(name)

    return test_list


class LogStreamOut(web.View):

    def import_model(self, model):
        try:
            m = importlib.import_module(
                'brome.model.{model}'.format(model=model)
            )
            return getattr(m, model.title())
        except ImportError:
            raise exceptions.ModelImportException(
                '{model} not found'.format(model=model)
            )

    @exception_handler()
    @require('login')
    async def post(self):
        essential_keys = [
            'skip',
            'model',
            'uid'
        ]

        # REQUEST
        req_data = await self.request.json()

        # Keys validation
        for key in essential_keys:
            if key not in req_data.keys():
                raise exceptions.InvalidRequestException(
                    "Missing '{key}' params".format(
                        key=key
                    )
                )

        skip = req_data.get('skip')
        model_name = req_data.get('model')
        uid = req_data.get('uid')

        if model_name not in ['testbatch', 'testinstance']:
            raise exceptions.InvalidRequestException(
                "Only model 'testbatch' and 'testinstance' are allowed"
            )

        model_class = self.import_model(model_name)
        query = self.request.db_session.query(model_class)\
            .filter(model_class.mongo_id == uid)

        if not query.count():
            raise exceptions.InvalidRequestException(
                "Instance not found for uid: {uid}".format(
                    uid=uid
                )
            )

        parent = query.one()

        log_file_path = parent.log_file_path
        if not log_file_path:
            raise exceptions.InvalidRequestException(
                "The instance 'log_file_path' is empty"
            )

        full_log_file_path = os.path.join(
            parent.root_path,
            log_file_path
        )

        results = []
        total = 0
        with open(full_log_file_path) as fd:
            for _ in range(skip):
                total += 1
                next(fd)

            results = fd.readlines()
            total += len(results)

        name = log_file_path\
            .rsplit(os.sep)[-1]\
            .rsplit('.')[0]\
            .replace('_', ' ')

        context = {
            'db_session': self.request.db_session,
            'ws_session': await get_session(self.request),
            'method': 'read'
        }

        # RESPONSE
        response_data = {
            'success': True,
            'total': total,
            'name': name,
            'parent': await parent.serialize(context),
            'results': results
        }
        return web.json_response(response_data)


class GetBromeConfig(web.View):

    @exception_handler()
    @require('login')
    async def get(self):
        # RESPONSE
        response_data = {
            'success': True,
            'config': BROME_CONFIG,
            'tests': get_tests()
        }
        return web.json_response(response_data)


class StartTestBatch(web.View):

    @exception_handler()
    @require('login')
    async def post(self):
        req_data = await self.request.json()

        tests = req_data.get('tests', get_tests())
        browsers = req_data['browsers']

        runner_path = os.path.join(
            BROME_CONFIG['project']['absolute_path'],
            BROME_CONFIG["brome"]["brome_executable_name"]
        )

        test_file_path = os.path.join(
            tempfile.gettempdir(),
            'test_file.yaml'
        )
        with open(test_file_path, 'w') as f:
            f.write(yaml.dump(tests, default_flow_style=False))

        commands = [
            sys.executable,
            runner_path,
            "run",
            "-r",
            ','.join(browsers),
            "--test-file",
            test_file_path
        ]
        subprocess.Popen(
            commands,
            stdout=open('runner.log', 'a'),
            stderr=open('runner.log', 'a')
        )
        # TODO return test batch id
        # RESPONSE
        response_data = {
            'success': True
        }
        return web.json_response(response_data)
