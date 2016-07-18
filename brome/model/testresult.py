from mongoalchemy.fields import (
    StringField,
    BoolField,
    AnythingField,
    ObjectIdField,
    DictField
)


from brome.model.basemodel import BaseModel


class Testresult(BaseModel):
    result = BoolField()
    browser_capabilities = DictField(AnythingField())
    browser_id = StringField()
    screenshot_path = StringField()
    videocapture_path = StringField()
    extra_data = DictField(StringField())
    title = StringField()

    test_id = ObjectIdField()
    test_instance_id = ObjectIdField()
    test_batch_id = ObjectIdField()

    def __repr__(self):
        try:
            return "Testresult <uid: {self.uid}><result: {self.result}><browser_id: {self.browser_id}><title: {self.title}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testresult uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['result'] = self.result
        data['browser_capabilities'] = self.browser_capabilities
        data['screenshot_path'] = self.screenshot_path
        data['videocapture_path'] = self.videocapture_path
        data['extra_data'] = self.extra_data
        data['title'] = self.title
        data['test_id'] = str(self.test_id)
        data['test_instance_id'] = str(self.test_instance_id)
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

        # RESULT
        result = data.get('result')
        if result is not None:
            self.result = result

        # BROWSER ID
        browser_id = data.get('browser_id')
        if browser_id is not None:
            self.browser_id = browser_id

        # BROWSER CAPABILITIES
        browser_capabilities = data.get('browser_capabilities')
        if browser_capabilities is not None:
            self.browser_capabilities = browser_capabilities

        # SCREENSHOT PATH
        screenshot_path = data.get('screenshot_path')
        if screenshot_path is not None:
            self.screenshot_path = screenshot_path
        else:
            self.screenshot_path = ''

        # VIDEOCAPTURE PATH
        videocapture_path = data.get('videocapture_path')
        if videocapture_path is not None:
            self.videocapture_path = videocapture_path
        else:
            self.videocapture_path = ''

        # EXTRA DATA
        extra_data = data.get('extra_data')
        if extra_data is not None:
            self.extra_data = extra_data
        else:
            self.extra_data = {}

        # TITLE
        title = data.get('title')
        if title is not None:
            self.title = title

        # TEST ID
        test_id = data.get('test_id')
        if test_id is not None:
            self.test_id = test_id

        # TEST INSTANCE ID
        test_instance_id = data.get('test_instance_id')
        if test_instance_id is not None:
            self.test_instance_id = test_instance_id

        # TEST BATCH ID
        test_batch_id = data.get('test_batch_id')
        if test_batch_id is not None:
            self.test_batch_id = test_batch_id

        db_session.save(self, safe=True)
