from mongoalchemy.fields import (
    DateTimeField,
    DictField,
    AnythingField,
    StringField,
    IntField,
    BoolField
)

from brome.model.basemodel import BaseModel
from brome.model.testcrash import Testcrash
from brome.model.testresult import Testresult
from brome.model.testscreenshot import Testscreenshot


class Testbatch(BaseModel):

    pid = IntField()
    killed = BoolField(default=False)
    total_tests = IntField()
    total_executing_tests = IntField(default=0)
    total_executed_tests = IntField(default=0)
    starting_timestamp = DateTimeField()
    ending_timestamp = DateTimeField(required=False)
    feature_session_video_capture = BoolField(default=False)
    feature_network_capture = BoolField(default=False)
    feature_bot_diaries = BoolField(default=False)
    feature_screenshots = BoolField(default=False)
    feature_instance_vnc = BoolField(default=False)
    feature_style_quality = BoolField(default=False)
    runner_metadata = DictField(AnythingField(), default=dict())
    log_file_path = StringField(default='')

    def __repr__(self):
        try:
            return "Testbatch <uid: {self.mongo_id}>".format(
                self=self
            )
        except AttributeError:
            return "Testbatch uninitialized"

    async def get_test_results(self, context):
        db_session = context.get('db_session')

        nb_test_result = db_session.query(Testresult)\
            .filter(Testresult.test_batch_id == self.get_uid())\
            .count()

        failed_tests_query = db_session.query(Testresult)\
            .filter(Testresult.test_batch_id == self.get_uid())\
            .filter(Testresult.result == False)  # noqa

        succeeded_test_query = db_session.query(Testresult)\
            .filter(Testresult.test_batch_id == self.get_uid())\
            .filter(Testresult.result == True)  # noqa

        data = {}
        data['nb_failed_test'] = failed_tests_query.count()
        data['nb_succeeded_test'] = succeeded_test_query.count()
        data['nb_test_result'] = nb_test_result
        data['failed_tests'] = []

        failed_tests_title = []
        for failed_test in failed_tests_query.all():
            if failed_test.title not in failed_tests_title:
                failed_tests_title.append(failed_test.title)
                data['failed_tests'].append(
                    await failed_test.serialize(context)
                )

        return data

    async def get_test_crashes(self, context):
        db_session = context.get('db_session')

        data = []

        test_crashes = db_session.query(Testcrash)\
            .filter(Testcrash.test_batch_id == self.get_uid())\
            .all()

        # TODO auto serialize
        for test_crash in test_crashes:
            data.append(await test_crash.serialize(context))

        return data

    async def get_nb_screenshot(self, context):
        db_session = context.get('db_session')

        query = db_session.query(Testscreenshot)\
            .filter(Testscreenshot.test_batch_id == self.mongo_id)

        return query.count()

    async def sanitize_data(self, context):
        return []

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['killed'] = self.killed
        data['total_tests'] = self.total_tests
        data['total_executed_tests'] = self.total_executed_tests
        data['total_executing_tests'] = self.total_executing_tests
        data['starting_timestamp'] = self.starting_timestamp.isoformat()
        data['nb_screenshot'] = await self.get_nb_screenshot(context)
        data['features'] = {
            'session_video_capture': self.feature_session_video_capture,
            'network_capture': self.feature_network_capture,
            'bot_diaries': self.feature_bot_diaries,
            'screenshots': self.feature_screenshots,
            'instance_vnc': self.feature_instance_vnc,
            'style_quality': self.feature_style_quality
        }
        data['runner_metadata'] = self.runner_metadata

        data['test_crashes'] = await self.get_test_crashes(context)
        data['test_results'] = await self.get_test_results(context)

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

        # FEATURES
        feature_session_video_capture = data.get(
            'feature_session_video_capture'
        )
        if feature_session_video_capture:
            self.feature_session_video_capture = feature_session_video_capture

        feature_network_capture = data.get('feature_network_capture')
        if feature_network_capture:
            self.feature_network_capture = feature_network_capture

        feature_bot_diaries = data.get('feature_bot_diaries')
        if feature_bot_diaries:
            self.feature_bot_diaries = feature_bot_diaries

        feature_screenshots = data.get('feature_screenshots')
        if feature_screenshots:
            self.feature_screenshots = feature_screenshots

        # RUNNER METADATA
        runner_metadata = data.get('runner_metadata')
        if runner_metadata:
            self.runner_metadata = runner_metadata

        db_session.save(self, safe=True)
