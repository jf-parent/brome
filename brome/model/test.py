from mongoalchemy.fields import (
    StringField
)

from brome.model.basemodel import BaseModel


class Test(BaseModel):

    test_id = StringField()
    name = StringField()

    def __repr__(self):
        try:
            return "Test <uid: {self.uid}>".format(
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

        # TEST_ID
        test_id = data.get('test_id')
        if test_id is not None:
            self.test_id = test_id

        # NAME
        name = data.get('name')
        if name:
            self.name = name

        db_session.save(self, safe=True)
