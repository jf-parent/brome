import os

from mongoalchemy.fields import (
    StringField,
    AnythingField,
    ObjectIdField,
    DictField
)


from brome.model.basemodel import BaseModel
from brome.model.testinstance import Testinstance
from brome.core import exceptions


class Testcrash(BaseModel):
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()

    extra_data = DictField(StringField(), default=dict())
    trace = StringField()
    title = StringField()

    root_path = StringField(default='')
    screenshot_path = StringField(default='')
    video_capture_path = StringField(default='')

    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testcrash <uid: {self.mongo_id}><browser_id: {self.browser_id}><title: {self.title}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testcrash uninitialized"

    def get_video_current_time(self, context):
        db_session = context.get('db_session')

        test_instance = db_session.query(Testinstance)\
            .filter(Testinstance.mongo_id == self.test_instance_id)\
            .one()

        created_ts = self.created_ts
        test_instance_created_ts = test_instance.created_ts

        current_time = (created_ts - test_instance_created_ts).total_seconds()

        return current_time

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['browser_capabilities'] = self.browser_capabilities
        data['screenshot_path'] = self.screenshot_path
        data['video_capture_path'] = self.video_capture_path
        data['video_capture_current_time'] = min(
            10,
            self.get_video_current_time(
                context
            )
        )
        data['root_path'] = self.root_path
        data['extra_data'] = self.extra_data
        data['title'] = self.title
        data['trace'] = self.trace.split(os.linesep)[:-1]
        data['test_instance_id'] = str(self.test_instance_id)
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

        # TRACE
        trace = data.get('trace')
        if trace is not None:
            self.trace = trace
        else:
            if is_new:
                raise exceptions.MissingModelValueException('trace')

        # BROWSER ID
        browser_id = data.get('browser_id')
        if browser_id is not None:
            self.browser_id = browser_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('browser_id')

        # BROWSER CAPABILITIES
        browser_capabilities = data.get('browser_capabilities')
        if browser_capabilities is not None:
            self.browser_capabilities = browser_capabilities
        else:
            if is_new:
                raise exceptions.MissingModelValueException(
                    'browser_capabilities'
                )

        # ROOT PATH
        root_path = data.get('root_path')
        if root_path is not None:
            self.root_path = root_path

        # SCREENSHOT PATH
        screenshot_path = data.get('screenshot_path')
        if screenshot_path is not None:
            self.screenshot_path = screenshot_path

        # VIDEO CAPTURE PATH
        video_capture_path = data.get('video_capture_path')
        if video_capture_path is not None:
            self.video_capture_path = video_capture_path

        # EXTRA DATA
        extra_data = data.get('extra_data')
        if extra_data is not None:
            self.extra_data = extra_data

        # TITLE
        title = data.get('title')
        if title is not None:
            self.title = title
        else:
            if is_new:
                raise exceptions.MissingModelValueException('title')

        # TEST INSTANCE ID
        test_instance_id = data.get('test_instance_id')
        if test_instance_id is not None:
            self.test_instance_id = test_instance_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('test_instance_id')

        # TEST BATCH ID
        test_batch_id = data.get('test_batch_id')
        if test_batch_id is not None:
            self.test_batch_id = test_batch_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('test_batch_id')

        db_session.save(self, safe=True)
