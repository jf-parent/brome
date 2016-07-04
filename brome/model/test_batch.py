from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class TestBatch(BaseModel):

    pid = IntField()
    killed = BoolField(default=False)
    total_tests = IntField()
    starting_timestamp = DateTimeField()
    ending_timestamp = DateTimeField(required=False)
