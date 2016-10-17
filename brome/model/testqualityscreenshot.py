from mongoalchemy.fields import (
    StringField,
    AnythingField,
    BoolField,
    ObjectIdField,
    EnumField,
    DictField
)

from brome.model.basemodel import BaseModel
from brome.core import exceptions


class Testqualityscreenshot(BaseModel):
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    file_path = StringField()
    root_path = StringField()
    location = EnumField(StringField(), 's3', 'local_file_system')
    extra_data = DictField(StringField(), default=dict())
    title = StringField()
    approved = BoolField(default=False)
    rejected = BoolField(default=False)

    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testqualityscreenshot <uid: {self.mongo_id}><test_batch_id: {self.test_batch_id}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testqualityscreenshot uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
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

        # BROWSER CAPABILITIES
        browser_capabilities = data.get('browser_capabilities')
        if browser_capabilities is not None:
            self.browser_capabilities = browser_capabilities
        else:
            if is_new:
                raise exceptions.MissingModelValueException(
                    'browser_capabilities'
                )

        # BROWSER ID
        browser_id = data.get('browser_id')
        if browser_id is not None:
            self.browser_id = browser_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('browser_id')

        # FILE PATH
        file_path = data.get('file_path')
        if file_path is not None:
            self.file_path = file_path
        else:
            if is_new:
                raise exceptions.MissingModelValueException('file_path')

        # ROOT PATH
        root_path = data.get('root_path')
        if root_path is not None:
            self.root_path = root_path
        else:
            if is_new:
                raise exceptions.MissingModelValueException('root_path')

        # LOCATION
        location = data.get('location')
        if location is not None:
            self.location = location
        else:
            if is_new:
                self.location = 'local_file_system'

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

        # APPROVED
        approved = data.get('approved')
        if approved is not None:
            self.approved = approved

        # REJECTED
        rejected = data.get('rejected')
        if rejected is not None:
            self.rejected = rejected

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
