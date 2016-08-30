import logging

from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import get_session

from brome.webserver.server.server_decorator import (
    exception_handler
)
from brome.webserver.server.auth import get_user_from_session
from brome.webserver.server.utils import generate_token

logger = logging.getLogger('bromewebserver')


async def set_csrf_token_session(session):
    if session.new:
        session['csrf_token'] = generate_token(20)


@aiohttp_jinja2.template('index.html')
async def index(request):
    logger.debug('index')
    return {}


@exception_handler()
async def api_get_session(request):
    logger.debug('get_session')

    session = await get_session(request)
    await set_csrf_token_session(session)
    data = await request.json()

    success = False
    token = session['csrf_token']
    user = None

    uid = session.get('uid')
    if uid:
        user = get_user_from_session(session, request.db_session)
        session['tz'] = data.get('user_timezone')
        if user.enable:
            context = {
                'user': user,
                'db_session': request.db_session,
                'method': 'read',
                'ws_session': session,
                'queue': request.app.queue
            }

            user = await user.serialize(context)
            success = True
        else:
            user.logout(session)
            user = None

    resp_data = {'success': success, 'user': user, 'token': token}
    return web.json_response(resp_data)
