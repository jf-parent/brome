from mongoalchemy.session import Session
from dateutil import tz

from brome.core.settings import BROME_CONFIG

async def db_handler(app, handler):
    async def middleware(request):
        if request.path.startswith('/api/'):
            request.db_session = Session.connect(
                BROME_CONFIG['database'].get("mongo_database_name"),
                timezone=tz.gettz('UTC')
            )

        response = await handler(request)
        return response

    return middleware
