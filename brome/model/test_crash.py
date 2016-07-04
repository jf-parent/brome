from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class TestCrash(BaseModel):
    timestamp = DateTimeField()
    browser_id = StringField()
    screenshot_path = StringField()
    videocapture_path = StringField()
    extra_data = DictField(StringField())
    trace = StringField()
    title = StringField()

    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()
