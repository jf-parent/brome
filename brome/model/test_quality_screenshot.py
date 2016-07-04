from mongoalchemy.fields import *  # noqa

from brome.model.basemodel import BaseModel

class TestQualityScreenshot(BaseModel):
    timestamp = DateTimeField()
    browser_id = StringField()
    screenshot_path = StringField()
    extra_data = DictField(StringField())
    title = StringField()
    approved = BoolField()
    rejected = BoolField()

    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()
