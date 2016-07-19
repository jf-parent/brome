import importlib
import logging
import os

from aiohttp import web
from brome.core import exceptions
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
