from datetime import datetime

from mongoalchemy.fields import (
    DateTimeField,
    BoolField,
    AnythingField,
    StringField,
    ObjectIdField,
    DictField
)


from brome.model.basemodel import BaseModel
from brome.core.utils import convert_tz_datetime
from brome.core import exceptions


class Testinstance(BaseModel):

    name = StringField()
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    starting_timestamp = DateTimeField(use_tz=True)
    ending_timestamp = DateTimeField(required=False, use_tz=True)
    terminated = BoolField(default=False)
    extra_data = DictField(StringField(), default=dict())

    root_path = StringField(default='')
    log_file_path = StringField(default='')
    network_capture_path = StringField(default='')
    video_capture_path = StringField(default='')
    # Bot diary

    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testinstance <uid: {self.mongo_id}><test_batch_id: {self.test_batch_id}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testinstance uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        ws_session = context.get('ws_session')

        data = {}
        data['uid'] = self.get_uid()
        data['name'] = self.name
        data['root_path'] = self.root_path
        data['log_file_path'] = self.log_file_path
        data['network_capture_path'] = self.network_capture_path
        data['video_capture_path'] = self.video_capture_path
        data['browser_capabilities'] = self.browser_capabilities
        data['starting_timestamp'] = convert_tz_datetime(
            self.starting_timestamp,
            ws_session.get('tz')
        ).isoformat()
        data['terminated'] = self.terminated
        if self.terminated:
            data['ending_timestamp'] = convert_tz_datetime(
                self.ending_timestamp,
                ws_session.get('tz')
            ).isoformat()
        else:
            data['ending_timestamp'] = False
        data['extra_data'] = self.extra_data
        data['test_batch_id'] = str(self.test_batch_id)
        return data

    async def method_autorized(self, context):
        method = context.get('method')
        if method in ['create', 'update', 'delete']:
            return False
        else:
            return True

    async def validate_and_save(self, context):
        data = context.get('data')
        db_session = context.get('db_session')

        is_new = await self.is_new()

        # NAME
        name = data.get('name')
        if name:
            self.name = name
        else:
            if is_new:
                raise exceptions.MissingModelValueException('name')

        # BROWSER ID
        browser_id = data.get('browser_id')
        if browser_id:
            self.browser_id = browser_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('browser_id')

        # BROWSER CAPABILITIES
        browser_capabilities = data.get('browser_capabilities')
        if browser_capabilities:
            self.browser_capabilities = browser_capabilities
        else:
            if is_new:
                raise exceptions.MissingModelValueException(
                    'browser_capabilities'
                )

        # STARTING TIMESTAMP
        starting_timestamp = data.get('starting_timestamp')
        if starting_timestamp:
            self.starting_timestamp = starting_timestamp
        else:
            if is_new:
                self.starting_timestamp = datetime.now()

        # ENDING TIMESTAMP
        ending_timestamp = data.get('ending_timestamp')
        if ending_timestamp:
            self.ending_timestamp = ending_timestamp

        # EXTRA DATA
        extra_data = data.get('extra_data')
        if extra_data is not None:
            self.extra_data = extra_data

        # ROOT PATH
        root_path = data.get('root_path')
        if root_path is not None:
            self.root_path = root_path

        # LOG FILE PATH
        log_file_path = data.get('log_file_path')
        if log_file_path is not None:
            self.log_file_path = log_file_path

        # NETWORk CAPTURE DATA
        network_capture_data = data.get('network_capture_data')
        if network_capture_data is not None:
            self.network_capture_data = network_capture_data

        # VIDEO CAPTURE PATH
        video_capture_path = data.get('video_capture_path')
        if video_capture_path is not None:
            self.video_capture_path = video_capture_path

        # TEST BATCH ID
        test_batch_id = data.get('test_batch_id')
        if test_batch_id:
            self.test_batch_id = test_batch_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('test_batch_id')

        db_session.save(self, safe=True)
