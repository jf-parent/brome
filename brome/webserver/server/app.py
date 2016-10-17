#! /usr/bin/env python

import os
import asyncio
from logging.handlers import TimedRotatingFileHandler
import logging

from redis import Redis
from rq import Queue
import aioredis
from aiohttp_session import redis_storage, session_middleware
import jinja2
import aiohttp_jinja2
from aiohttp import web

from brome.webserver.server.routes import routes
from brome.webserver.server.middlewares import db_handler
from brome.core.settings import BROME_CONFIG

logger = logging.getLogger('bromewebserver')

async def shutdown(server, app, handler):

    server.close()
    await server.wait_closed()
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()
    await app.redis_pool.clear()


async def init(loop):
    ROOT = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..'
    )

    # CONFIG
    logger = logging.getLogger('bromewebserver')
    logger.debug('Env: {env}'.format(env=BROME_CONFIG['webserver']['env']))

    # LOGGER
    logger.setLevel(
        getattr(logging, BROME_CONFIG['webserver'].get('log_level', 'INFO'))
    )

    formatter = logging.Formatter(
        '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    # StreamHandler
    if BROME_CONFIG['webserver'].get('streamlogger', True):
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # FileHandler
    if BROME_CONFIG['webserver'].get('filelogger', False):
        if BROME_CONFIG['webserver'].get('log_file_path'):
            fh = TimedRotatingFileHandler(
                BROME_CONFIG['webserver'].get('log_file_path'),
                when="midnight"
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    # SESSION
    redis_pool = await aioredis.create_pool(('localhost', 6379))
    storage = redis_storage.RedisStorage(redis_pool)
    app = web.Application(loop=loop, middlewares=[
        session_middleware(storage),
        db_handler
    ])

    app.redis_pool = redis_pool

    # QUEUE
    app.queue = Queue(connection=Redis())

    handler = app.make_handler()

    # ROUTES
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    if BROME_CONFIG['webserver'].get('env', 'production') in \
            ['development']:
        static_path = os.path.join(ROOT, 'dist-dev')
        try:
            if BROME_CONFIG['project']['test_batch_result_path']:
                os.symlink(
                    os.path.join(
                        BROME_CONFIG['project']['test_batch_result_path'],
                        'tb_results'
                    ),
                    os.path.join(static_path, 'static', 'tb_results')
                )
                if BROME_CONFIG['webserver'].get('env') != 'test':
                    logger.info(
                        "Serving test batch results from symlink: %s"
                        % BROME_CONFIG['project']['test_batch_result_path']
                    )
        except FileExistsError:
            pass

    elif BROME_CONFIG['webserver']['env'] == 'test':
        # NOTE don't serve any static in test mode
        pass
    else:
        if BROME_CONFIG['webserver'].get('release', 'latest') == 'latest':
            latest_version_path = os.path.join(
                ROOT,
                'releases',
                'latest.txt'
            )
            if os.path.exists(latest_version_path):
                with open(latest_version_path, 'r') as fd:
                    release_version = fd.read()
            else:
                raise Exception("The latest.txt file doesn't exists")
        else:
            release_version = BROME_CONFIG['webserver'].get('release')

        static_path = os.path.join(ROOT, 'releases', release_version)

    app.router.add_static('/', static_path, name='static')
    if BROME_CONFIG['webserver'].get('env') != 'test':
        logger.info(
            "Serving static: {static_path}"
            .format(
                static_path=static_path
            )
        )

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(static_path))

    # PREPARE HOOK
    async def after_request(request, response):
        if hasattr(request, 'db_session'):
            request.db_session.end()
            # request.db_session.db.connection.disconnect()

    app.on_response_prepare.append(after_request)

    serv_generator = loop.create_server(
        handler,
        BROME_CONFIG['webserver'].get('host'),
        BROME_CONFIG['webserver'].get('port')
    )

    return serv_generator, handler, app


def run_app():
    loop = asyncio.get_event_loop()

    serv_generator, handler, app = loop.run_until_complete(
        init(loop)
    )

    serv = loop.run_until_complete(serv_generator)

    logger.info('Server listening at %s' % str(serv.sockets[0].getsockname()))
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        logger.debug('Server stopping...')

    finally:
        loop.run_until_complete(shutdown(serv, app, handler))
        loop.close()

    logger.debug('Server stopped')

if __name__ == '__main__':
    run_app()
