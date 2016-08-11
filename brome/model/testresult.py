from mongoalchemy.fields import (
    StringField,
    BoolField,
    AnythingField,
    ObjectIdField,
    DictField
)


from brome.model.basemodel import BaseModel
from brome.model.test import Test
from brome.core import exceptions


class Testresult(BaseModel):
    result = BoolField()
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    title = StringField()

    root_path = StringField(default='')
    screenshot_path = StringField(default='')
    video_capture_path = StringField(default='')

    extra_data = DictField(StringField(), default=dict())

    test_id = ObjectIdField(required=False)
    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testresult <uid: {self.uid}><result: {self.result}><browser_id: {self.browser_id}><title: {self.title}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testresult uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        db_session = context.get('db_session')
        data = {}
        data['uid'] = self.get_uid()
        data['result'] = self.result
        data['browser_capabilities'] = self.browser_capabilities
        data['root_path'] = self.root_path
        data['screenshot_path'] = self.screenshot_path
        data['video_capture_path'] = self.video_capture_path
        # TODO video_capture_current_time
        # data['video_capture_current_time'] = video_capture_current_time
        data['extra_data'] = self.extra_data
        data['title'] = self.title
        if hasattr(self, 'test_id'):
            test = db_session.query(Test)\
                .filter(Test.mongo_id == self.test_id)\
                .one()
            data['test_id'] = test.test_id
        else:
            data['test_id'] = False
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

        # RESULT
        result = data.get('result')
        if result is not None:
            self.result = result
        else:
            if is_new:
                raise exceptions.MissingModelValueException('result')

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

        # VIDEOCAPTURE PATH
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

        # TEST ID
        test_id = data.get('test_id')
        if test_id is not None:
            self.test_id = test_id

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
