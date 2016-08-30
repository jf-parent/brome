import logging

from aiohttp_session import get_session
from aiohttp import web

from brome.core import exceptions
from brome.model.user import User
from brome.core.settings import BROME_CONFIG
from brome.webserver.server.server_decorator import (
    require,
    exception_handler,
    csrf_protected
)
from brome.webserver.server.auth import set_session, get_user_from_session

logger = logging.getLogger('bromewebserver')


class Login(web.View):

    @exception_handler()
    @csrf_protected()
    async def post(self):
        try:
            data = await self.request.json()
            email = data['email']
            password = data['password']
        except:
            raise exceptions.InvalidRequestException('No json send')

        query = self.request.db_session.query(User)\
            .filter(User.email == email)
        if query.count():
            user = query.one()
            is_password_valid = await user.check_password(password)
            is_enable = user.enable
            if is_password_valid and is_enable:
                await set_session(user, self.request)
                session = await get_session(self.request)
                session['tz'] = data.get('user_timezone')

                context = {
                    'db_session': self.request.db_session,
                    'method': 'read',
                    'queue': self.request.app.queue
                }

                resp_data = {
                    'success': True,
                    'token': session['csrf_token'],
                    'user': await user.serialize(context)
                }
            else:
                raise exceptions.WrongEmailOrPasswordException()
        else:
            raise exceptions.WrongEmailOrPasswordException(
                "Wrong email: '{email}'".format(email=email)
            )

        return web.json_response(resp_data)


class Register(web.View):

    @exception_handler()
    @csrf_protected()
    async def post(self):
        try:
            data = await self.request.json()
        except:
            raise exceptions.InvalidRequestException('No json send')

        context = {
            'db_session': self.request.db_session,
            'method': 'create',
            'queue': self.request.app.queue
        }

        registration_token = data.get('registration_token')
        if registration_token != \
                BROME_CONFIG['webserver']['registration_token']:
            raise exceptions.InvalidRegistrationTokenException()

        # INIT USER
        user = User()
        context['data'] = data
        sane_data = await user.sanitize_data(context)
        context['data'] = sane_data
        await user.validate_and_save(context)

        # SET SESSION
        await set_session(user, self.request)
        session = await get_session(self.request)
        session['tz'] = data.get('user_timezone')

        context['method'] = 'read'
        context['user'] = user
        resp_data = {
            'success': True,
            'user': await user.serialize(context),
            'token': session['csrf_token']
        }
        return web.json_response(resp_data)


class Logout(web.View):

    @exception_handler()
    @require('login')
    @csrf_protected()
    async def post(self):
        session = await get_session(self.request)
        user = get_user_from_session(session, self.request.db_session)
        user.logout(session)
        resp_data = {'success': True}
        return web.json_response(resp_data)
