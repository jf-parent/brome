from mongoalchemy.fields import (
    StringField,
    AnythingField,
    ObjectIdField,
    EnumField,
    DictField
)

from brome.model.basemodel import BaseModel
from brome.webserver.server import exceptions


class Testscreenshot(BaseModel):
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    relative_path = StringField()
    full_path = StringField()
    location = EnumField(StringField(), 's3', 'local_file_system')
    extra_data = DictField(StringField())
    title = StringField()

    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testscreenshot <uid: {self.mongo_id}><test_batch_id: {self.test_batch_id}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testscreenshot uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['relative_path'] = self.relative_path
        data['full_path'] = self.full_path
        data['title'] = self.title
        data['browser_capabilities'] = self.browser_capabilities
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

        # BROWSER ID
        browser_id = data.get('browser_id')
        if browser_id:
            self.browser_id = browser_id

        # BROWSER CAPABILITIES
        browser_capabilities = data.get('browser_capabilities')
        if browser_capabilities:
            self.browser_capabilities = browser_capabilities

        # RELATIVE_PATH
        relative_path = data.get('relative_path')
        if relative_path:
            self.relative_path = relative_path
        else:
            raise exceptions.MissingModelValueException('relative_path')

        # FULL_PATH
        full_path = data.get('full_path')
        if full_path:
            self.full_path = full_path
        else:
            raise exceptions.MissingModelValueException('full_path')

        # LOCATION
        location = data.get('location')
        if location:
            self.location = location
        else:
            self.location = 'local_file_system'

        # EXTRA_DATA
        extra_data = data.get('extra_data')
        if extra_data:
            self.extra_data = extra_data
        else:
            self.extra_data = {}

        # TITLE
        title = data.get('title')
        if title:
            self.title = title
        else:
            self.title = 'N/A'

        # TEST_INSTANCE_ID
        test_instance_id = data.get('test_instance_id')
        if test_instance_id:
            self.test_instance_id = test_instance_id
        else:
            raise exceptions.MissingModelValueException('test_instance_id')

        # TEST_BATCH_ID
        test_batch_id = data.get('test_batch_id')
        if test_batch_id:
            self.test_batch_id = test_batch_id
        else:
            raise exceptions.MissingModelValueException('test_batch_id')

        db_session.save(self, safe=True)
