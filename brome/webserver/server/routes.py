from brome.webserver.server.public.views import (
    index,
    api_get_session,
    api_validate_reset_password_token,
    api_send_reset_password_token
)
from brome.webserver.server.auth.views import (
    api_reset_password,
    Logout,
    Login,
    api_admin,
    api_confirm_email,
    Register

)
from brome.webserver.server.crud.views import CRUD
from brome.webserver.server.brome_api.views import LogStreamOut, TestBatch

routes = [
    # CLIENT ROUTE => not /api/* and not /static/*
    ('GET', r'/{to:(?!api)(?!static).*}', index, 'index'),

    # API ROUTES
    ('GET', '/api/get_session', api_get_session, 'get_session'),
    ('GET', '/api/admin', api_admin, 'admin'),
    ('POST', '/api/confirm_email', api_confirm_email, 'api_confirm_email'),
    ('POST', '/api/reset_password', api_reset_password, 'api_reset_password'),
    (
        'POST',
        '/api/validate_reset_password_token',
        api_validate_reset_password_token,
        'api_validate_reset_password_token'
    ),
    (
        'POST',
        '/api/send_reset_password_token',
        api_send_reset_password_token,
        'api_send_reset_password_token'
    ),
    ('*', '/api/crud', CRUD, 'api_crud'),
    ('*', '/api/logstreamout', LogStreamOut, 'api_log_stream_out'),
    ('*', '/api/testbatch', TestBatch, 'api_test_batch'),
    ('*', '/api/login', Login, 'api_login'),
    ('*', '/api/register', Register, 'api_register'),
    ('*', '/api/logout', Logout, 'api_logout'),
]