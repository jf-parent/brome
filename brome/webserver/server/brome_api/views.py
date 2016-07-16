import importlib
import logging
import os

from aiohttp import web
from aiohttp_session import get_session

from brome.webserver.server.auth import get_user_from_session
from brome.model.testcrash import Testcrash
from brome.model.testresult import Testresult
from brome.model.testinstance import Testinstance
from brome.webserver.server import exceptions
from brome.webserver.server.server_decorator import (
    require,
    exception_handler
)

logger = logging.getLogger('bromewebserver')


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

        instance = query.one()

        log_file_path = instance.log_file_path

        if not log_file_path:
            raise exceptions.InvalidRequestException(
                "The instance 'log_file_path' is empty"
            )

        results = []
        total = 0
        with open(log_file_path) as fd:
            for _ in range(skip):
                total += 1
                next(fd)

            results = fd.readlines()
            total += len(results)

        name = log_file_path\
            .rsplit(os.sep)[-1]\
            .rsplit('.')[0]\
            .replace('_', ' ')

        # RESPONSE
        response_data = {
            'success': True,
            'total': total,
            'name': name,
            'results': results
        }
        return web.json_response(response_data)


class TestBatch(web.View):

    @exception_handler()
    @require('login')
    async def post(self):
        essential_keys = [
            'method',
            'limit',
            'skip',
            'uid'
        ]

        session = await get_session(self.request)
        author = get_user_from_session(session, self.request.db_session)

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

        method = req_data.get('method')
        uid = req_data.get('uid')
        skip = req_data.get('skip')
        limit = req_data.get('limit')

        method_list = [
            'list_test_instances',
            'list_network_captures',
            'list_screenshot',
            'list_test_results',
            'list_crashes_reports'
        ]
        if method not in method_list:
            raise exceptions.InvalidRequestException(
                'Invalid method'
            )

        db_session = self.request.db_session
        context = {
            'method': 'read',
            'db_session': db_session,
            'author': author
        }
        results = []
        total = 0

        # CRASHES LIST
        if method == 'list_crashes_reports':
            total = db_session.query(Testcrash)\
                .filter(Testcrash.test_batch_id == uid)\
                .count()

            _results = db_session.query(Testcrash)\
                .filter(Testcrash.test_batch_id == uid)\
                .skip(skip)\
                .limit(limit)\
                .all()

            for result in _results:
                results.append(await result.serialize(context))

        # TEST RESULTS
        elif method == 'list_test_results':
            total = db_session.query(Testresult)\
                .filter(Testresult.test_batch_id == uid)\
                .count()

            _results = db_session.query(Testresult)\
                .filter(Testresult.test_batch_id == uid)\
                .skip(skip)\
                .limit(limit)\
                .ascending('result')\
                .all()

            for result in _results:
                results.append(await result.serialize(context))

        # SCREENSHOTS
        elif method == 'list_screenshot':
            # TODO
            raise NotImplementedError()

        # NETWORK CAPTURES
        elif method == 'list_network_captures':
            # TODO
            raise NotImplementedError()

        # TEST INSTANCES
        elif method == 'list_test_instances':
            total = db_session.query(Testinstance)\
                .filter(Testinstance.test_batch_id == uid)\
                .count()

            _results = db_session.query(Testinstance)\
                .filter(Testinstance.test_batch_id == uid)\
                .skip(skip)\
                .limit(limit)\
                .ascending('name')\
                .all()

            for result in _results:
                results.append(await result.serialize(context))

        # RESPONSE
        response_data = {
            'success': True,
            'total': total,
            'results': results
        }
        return web.json_response(response_data)
