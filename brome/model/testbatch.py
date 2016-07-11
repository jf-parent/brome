from mongoalchemy.fields import (
    DateTimeField,
    IntField,
    BoolField
)

from brome.model.basemodel import BaseModel


class Testbatch(BaseModel):

    pid = IntField()
    killed = BoolField(default=False)
    total_tests = IntField()
    starting_timestamp = DateTimeField()
    ending_timestamp = DateTimeField(required=False)
    feature_session_video_capture = BoolField(default=False)
    feature_network_capture = BoolField(default=False)
    feature_bot_diaries = BoolField(default=False)
    feature_screenshots = BoolField(default=False)

    def __repr__(self):
        try:
            return "Testbatch <uid: {self.mongo_id}>".format(
                self=self
            )
        except AttributeError:
            return "Testbatch uninitialized"

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['killed'] = self.killed
        data['total_tests'] = 110  # TODO
        data['total_executed_tests'] = 43  # TODO
        data['total_executing_tests'] = 2  # TODO
        data['starting_timestamp'] = self.starting_timestamp.isoformat()
        data['features'] = {
            'session_video_capture': self.feature_session_video_capture,
            'network_capture': self.feature_network_capture,
            'bot_diaries': self.feature_bot_diaries,
            'screenshots': self.feature_screenshots,
        }
        # Terminated test batch
        if hasattr(self, 'ending_timestamp'):
            data['ending_timestamp'] = self.ending_timestamp.isoformat()
            data['terminated'] = True

        # Running test batch
        else:
            data['ending_timestamp'] = False
            data['terminated'] = False
        return data

    async def method_autorized(self, context):
        author = context.get('author')
        method = context.get('method')
        if method in ['create', 'update']:
            return False
        else:
            if method == 'delete':
                if author.role == 'admin':
                    return True
                else:
                    return False
            else:
                return True

    async def validate_and_save(self, context):
        data = context.get('data')
        db_session = context.get('db_session')

        # Killed
        killed = data.get('killed')
        if killed is not None:
            self.killed = killed

        # PID
        pid = data.get('pid')
        if pid is not None:
            self.pid = pid

        # TOTAL TESTS
        total_tests = data.get('total_tests')
        if total_tests is not None:
            self.total_tests = total_tests

        # STARTING TIMESTAMP
        starting_timestamp = data.get('starting_timestamp')
        if starting_timestamp:
            self.starting_timestamp = starting_timestamp

        # ENDING TIMESTAMP
        ending_timestamp = data.get('ending_timestamp')
        if ending_timestamp:
            self.ending_timestamp = ending_timestamp

        db_session.save(self, safe=True)
