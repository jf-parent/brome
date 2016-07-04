from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class TestInstance(BaseModel):

    name = StringField()

    starting_timestamp = DateTimeField()
    ending_timestamp = DateTimeField(required=False)
    extra_data = DictField(StringField())

    test_batch_id = ObjectIdField()
