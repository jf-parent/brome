from mongoalchemy.fields import (
    StringField
)

from brome.model.basemodel import BaseModel
from brome.core import exceptions


class Test(BaseModel):

    test_id = StringField()
    name = StringField()

    def __repr__(self):
        try:
            return "Test <test_id: {self.test_id}><name: {self.name}>".format(
                self=self
            )
        except AttributeError:
            return "Test uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['test_id'] = self.test_id
        data['name'] = self.name
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

        is_new = self.is_new()

        # TEST ID
        test_id = data.get('test_id')
        if test_id is not None:
            self.test_id = test_id
        else:
            if is_new:
                raise exceptions.MissingModelValueException('test_id')

        # NAME
        name = data.get('name')
        if name:
            self.name = name
        else:
            if is_new:
                raise exceptions.MissingModelValueException('name')

        db_session.save(self, safe=True)
