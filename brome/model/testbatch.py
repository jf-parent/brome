from datetime import datetime
import shutil

from mongoalchemy.fields import (
    DateTimeField,
    DictField,
    AnythingField,
    StringField,
    IntField,
    BoolField
)

from brome.core.utils import convert_tz_datetime
from brome.model.basemodel import BaseModel
from brome.model.testinstance import Testinstance
from brome.model.testcrash import Testcrash
from brome.model.testresult import Testresult
from brome.model.testscreenshot import Testscreenshot
from brome.core import exceptions


class Testbatch(BaseModel):

    friendly_name = StringField()
    pid = IntField()
    killed = BoolField(default=False)
    total_tests = IntField()
    starting_timestamp = DateTimeField(use_tz=True)
    ending_timestamp = DateTimeField(required=False, use_tz=True)
    terminated = BoolField(default=False)
    feature_session_video_capture = BoolField(default=False)
    feature_network_capture = BoolField(default=False)
    feature_bot_diaries = BoolField(default=False)
    feature_screenshots = BoolField(default=False)
    feature_instance_vnc = BoolField(default=False)
    feature_style_quality = BoolField(default=False)
    runner_metadata = DictField(AnythingField(), default=dict())
    root_path = StringField(default='')
    log_file_path = StringField(default='')

    def __repr__(self):
        try:
            return "Testbatch <uid: {self.mongo_id}><friendly_name: {self.friendly_name}>".format(  # noqa
                self=self
            )
        except AttributeError:
            return "Testbatch uninitialized"

    def add_milestone(self, milestone_id, values=None, index=None):
        if 'milestones' not in self.runner_metadata.keys():
            self.runner_metadata['milestones'] = {}

        effective_index = index
        effective_values = values
        if not index:
            effective_index = len(self.runner_metadata['milestones'])

        if not values:
            effective_values = {}

        self.runner_metadata['milestones'][milestone_id] = {
            'msg_id': milestone_id,
            'index': effective_index,
            'values': effective_values
        }

    def update_milestone(self, milestone_id, values):
        self.runner_metadata['milestones'][milestone_id]['values'] = values

    async def get_browser_ids(self, context):
        db_session = context.get('db_session')

        browser_ids = []

        unique_browser_ids = db_session.query(Testinstance)\
            .filter(Testinstance.test_batch_id == self.get_uid())\
            .distinct('browser_id')

        for browser_id in unique_browser_ids:
            capabilities = db_session.query(Testinstance)\
                .filter(Testinstance.test_batch_id == self.get_uid())\
                .filter(Testinstance.browser_id == browser_id)\
                .first().browser_capabilities

            browser_id_dict = {
                'id': browser_id,
                'capabilities': capabilities
            }
            browser_ids.append(browser_id_dict)

        return browser_ids

    async def get_milestones(self):
        data = []
        if 'milestones' in self.runner_metadata.keys():
            sorted_milestones = sorted(
                self.runner_metadata['milestones'].values(),
                key=lambda x: x['index']
            )
            for milestone in sorted_milestones:
                data.append({
                    'values': milestone['values'],
                    'msgId': milestone['msg_id']
                })

        return data

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

    async def get_total_executings_tests(self, context):
        db_session = context.get('db_session')

        return db_session.query(Testinstance)\
            .filter(Testinstance.terminated == False)\
            .filter(Testinstance.test_batch_id == self.mongo_id)\
            .count()  # noqa

    async def get_total_executed_tests(self, context):
        db_session = context.get('db_session')

        return db_session.query(Testinstance)\
            .filter(Testinstance.terminated == True)\
            .filter(Testinstance.test_batch_id == self.mongo_id)\
            .count()  # noqa

    async def get_test_crashes(self, context):
        db_session = context.get('db_session')

        data = []

        test_crashes = db_session.query(Testcrash)\
            .filter(Testcrash.test_batch_id == self.get_uid())\
            .ascending('title')\
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
        author = context.get('author')
        data = context.get('data')

        if author:
            if author.role == 'admin':
                return data
            else:
                editable_fields = [
                    'killed'
                ]
        else:
            editable_fields = []

        return {k: data[k] for k in data if k in editable_fields}

    async def serialize(self, context):
        ws_session = context.get('ws_session')

        data = {}
        data['uid'] = self.get_uid()
        data['friendly_name'] = self.friendly_name
        data['killed'] = self.killed
        data['total_tests'] = self.total_tests
        data['browser_ids'] = await self.get_browser_ids(context)
        data['total_executed_tests'] = await self.get_total_executed_tests(context)  # noqa
        data['total_executing_tests'] = await self.get_total_executings_tests(context)  # noqa
        data['starting_timestamp'] = convert_tz_datetime(
            self.starting_timestamp,
            ws_session['tz']
        ).isoformat()
        data['nb_screenshot'] = await self.get_nb_screenshot(context)
        data['root_path'] = self.root_path
        data['log_file_path'] = self.log_file_path
        data['features'] = {
            'session_video_capture': self.feature_session_video_capture,
            'network_capture': self.feature_network_capture,
            'bot_diaries': self.feature_bot_diaries,
            'screenshots': self.feature_screenshots,
            'instance_vnc': self.feature_instance_vnc,
            'style_quality': self.feature_style_quality
        }
        data['milestones'] = await self.get_milestones()

        data['test_crashes'] = await self.get_test_crashes(context)
        data['test_results'] = await self.get_test_results(context)

        data['terminated'] = self.terminated
        # Terminated test batch
        if self.terminated:
            data['ending_timestamp'] = convert_tz_datetime(
                self.ending_timestamp,
                ws_session['tz']
            ).isoformat()

        # Running test batch
        else:
            data['ending_timestamp'] = False

        return data

    async def method_autorized(self, context):
        author = context.get('author')
        method = context.get('method')

        if method in ['create']:
            return False
        else:
            if author:
                return True
            else:
                return False

    async def validate_and_save(self, context):
        data = context.get('data')
        db_session = context.get('db_session')

        is_new = await self.is_new()

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
        else:
            if is_new:
                raise exceptions.MissingModelValueException('total_tests')

        # FRIENDLY NAME
        friendly_name = data.get('friendly_name')
        if friendly_name:
            self.friendly_name = friendly_name
        else:
            if is_new:
                raise exceptions.MissingModelValueException('total_tests')

        # STARTING TIMESTAMP
        starting_timestamp = data.get('starting_timestamp')
        if starting_timestamp:
            self.starting_timestamp = starting_timestamp
        else:
            if is_new:
                self.starting_timestamp = datetime.now()

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

        # LOG FILE PATH
        log_file_path = data.get('log_file_path')
        if log_file_path:
            self.log_file_path = log_file_path

        # ROOT PATH
        root_path = data.get('root_path')
        if root_path:
            self.root_path = root_path

        db_session.save(self, safe=True)

    async def after_delete(self, context):
        shutil.rmtree(self.root_path)
