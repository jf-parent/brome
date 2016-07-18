from mongoalchemy.fields import (
    StringField,
    AnythingField,
    BoolField,
    ObjectIdField,
    EnumField,
    DictField
)

from brome.model.basemodel import BaseModel


class Testqualityscreenshot(BaseModel):
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    relative_path = StringField()
    full_path = StringField()
    location = EnumField(StringField(), 's3', 'local_file_system')
    extra_data = DictField(StringField())
    title = StringField()
    approved = BoolField()
    rejected = BoolField()

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
        # data = context.get('data')
        db_session = context.get('db_session')

        # TODO
        db_session.save(self, safe=True)
