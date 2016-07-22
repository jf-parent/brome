from brome.webserver.server.public.views import (
    index,
    api_get_session
)
from brome.webserver.server.auth.views import (
    Logout,
    Login,
    Register

)
from brome.webserver.server.crud.views import CRUD
from brome.webserver.server.brome_api.views import (
    LogStreamOut,
    GetBromeConfig,
    StartTestBatch
)

routes = [
    # CLIENT ROUTE => not /api/* and not /static/*
    ('GET', r'/{to:(?!api)(?!static).*}', index, 'index'),

    # API ROUTES
    ('GET', '/api/get_session', api_get_session, 'get_session'),
    ('*', '/api/crud', CRUD, 'api_crud'),
    ('*', '/api/getbromeconfig', GetBromeConfig, 'api_get_brome_config'),
    ('*', '/api/starttestbatch', StartTestBatch, 'api_start_test_batch'),
    ('*', '/api/logstreamout', LogStreamOut, 'api_log_stream_out'),
    ('*', '/api/login', Login, 'api_login'),
    ('*', '/api/register', Register, 'api_register'),
    ('*', '/api/logout', Logout, 'api_logout'),
]
