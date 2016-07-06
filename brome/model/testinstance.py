from mongoalchemy.fields import (
    DateTimeField,
    StringField,
    ObjectIdField,
    DictField
)


from brome.model.basemodel import BaseModel


class Testinstance(BaseModel):

    name = StringField()

    starting_timestamp = DateTimeField()
    ending_timestamp = DateTimeField(required=False)
    extra_data = DictField(StringField())

    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testinstance <uid: {self.uid}><test_batch_id: {self.test_batch_id}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testinstance uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['name'] = self.name
        data['starting_timestamp'] = self.starting_timestamp.isoformat()
        if hasattr(self, 'ending_timestamp'):
            data['ending_timestamp'] = self.ending_timestamp.isoformat()
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

        # NAME
        name = data.get('name')
        if name:
            self.name = name

        # STARTING TIMESTAMP
        starting_timestamp = data.get('starting_timestamp')
        if starting_timestamp:
            self.starting_timestamp = starting_timestamp

        # ENDING TIMESTAMP
        ending_timestamp = data.get('ending_timestamp')
        if ending_timestamp:
            self.ending_timestamp = ending_timestamp

        # EXTRA DATA
        extra_data = data.get('extra_data')
        if extra_data is not None:
            self.extra_data = extra_data
        else:
            self.extra_data = {}

        # TEST BATCH ID
        test_batch_id = data.get('test_batch_id')
        if test_batch_id:
            self.test_batch_id = test_batch_id

        db_session.save(self, safe=True)
