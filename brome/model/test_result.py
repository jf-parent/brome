from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class TestResult(BaseModel):
    result = BoolField()
    timestamp = DateTimeField() # TODO use the created_ts instead
    browser_id = StringField()
    screenshot_path = StringField()
    videocapture_path = StringField()
    extra_data = DictField(StringField())
    title = StringField()

    test_id = ObjectIdField()
    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()
