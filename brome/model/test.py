from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class Test(BaseModel):

    test_id = StringField()
    name = StringField()
