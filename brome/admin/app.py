import os
import importlib
import base64
import logging
# from logging.handlers import TimedRotatingFileHandler
import sys
import asyncio

# from IPython import embed
from flask_admin.form import Select2Widget
from cryptography import fernet
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_mongoengine.wtf.fields import DictField
from wtforms import form, fields, validators
from flask import Flask, url_for, redirect, request, flash
import flask_admin as admin
from flask_admin import expose, helpers
import flask_login as login
from flask_admin.babel import gettext
from flask_admin.contrib.pymongo import ModelView
from flask.ext.session import Session

# PATH

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.append(ROOT)

from brome.model.user import User  # noqa
from brome.model.testbatch import Testbatch  # noqa
from brome.core.utils import DbSessionContext  # noqa
from brome.core.settings import BROME_CONFIG  # noqa
from brome.core import exceptions  # noqa

# LOOP

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

config = BROME_CONFIG['webserver']['admin']

# LOGGING

# #DISABLE werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# BROME ADMIN
logger = logging.getLogger('brome_admin')
logger.setLevel(getattr(logging, config.get('log_level', 'INFO')))

formatter = logging.Formatter(
    '[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# StreamHandler
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

"""
# FileHandler
fh = TimedRotatingFileHandler(
    os.path.join(ROOT, 'logs', 'admin_server.log'),
    when="midnight"
)
fh.setFormatter(formatter)
logger.addHandler(fh)
"""

# MONGO
mongo_client = MongoClient()
db = mongo_client[BROME_CONFIG['database'].get('mongo_database_name')]

# APP
app = Flask(__name__)

# SECRET KEY
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
app.config['SECRET_KEY'] = secret_key

# SESSION
app.config['SESSION_TYPE'] = 'redis'
sess = Session()
sess.init_app(app)


class BaseView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

    def create_model(self, form):
        model = form.data
        self.on_model_change(form, model, True)
        return True

    def update_model(self, form, model):
        self.on_model_change(form, model, False)
        return True

    def on_model_change(self, form, model, is_created):
        logger.info("on_model_change")
        with DbSessionContext(
            BROME_CONFIG['database'].get('mongo_database_name')
                ) as session:
            try:
                m = importlib.import_module(
                    'brome.model.{model}'
                    .format(model=self.name.lower())
                )
                model_class = getattr(m, self.name)

                if not is_created:
                    model_obj = session.query(model_class)\
                        .filter(model_class.mongo_id == model['_id'])\
                        .one()
                else:
                    model_obj = model_class()

                context = {}
                context['db_session'] = session
                context['author'] = login.current_user
                context['data'] = form.data
                context['save'] = True

                loop.run_until_complete(model_obj.validate_and_save(context))

                pk = model_obj.get_uid()
                self.coll.update({'_id': pk}, model)

            except Exception as e:
                if isinstance(e, exceptions.ServerBaseException):
                    flash(
                      gettext(
                        'Failed to update record. %(exception)s(%(error)s)',
                        exception=e.get_name(),
                        error=e
                      ),
                      'error'
                    )
                else:
                    flash(
                        gettext(
                            'Failed to update record. %(error)s',
                            error=e
                        ),
                        'error'
                    )
                return False
            else:
                self.after_model_change(form, model, True)

            return True


class TestBatchUidToFriendlyNameView(BaseView):
    def get_list(self, *args, **kwargs):
        count, data = super(
            TestBatchUidToFriendlyNameView, self
        ).get_list(*args, **kwargs)

        query = {'_id': {'$in': [x['test_batch_id'] for x in data]}}
        test_batchs = db.Testbatch.find(
            query,
            projection={'friendly_name': True}
        )

        test_batch_map = dict(
            (x['_id'], x['friendly_name']) for x in test_batchs
        )

        for item in data:
            item['test_batch_friendly_name'] = \
                test_batch_map.get(item['test_batch_id'])

        return count, data

    def _feed_user_choices(self, form):
        test_batchs = db.Testbatch.find(projection={'friendly_name': True})
        form.test_batch_id.choices = [
            (str(x['_id']), x['friendly_name']) for x in test_batchs
        ]
        return form

    def create_form(self):
        form = super(TestBatchUidToFriendlyNameView, self).create_form()
        return self._feed_user_choices(form)

    def edit_form(self, obj):
        form = super(TestBatchUidToFriendlyNameView, self).edit_form(obj)
        return self._feed_user_choices(form)

    def on_model_change(self, form, model, is_created):
        test_batch_id = model.get('test_batch_id')
        model['test_batch_id'] = ObjectId(test_batch_id)

        return super(TestBatchUidToFriendlyNameView, self).on_model_change(
            form,
            model,
            is_created
        )

    def _search(self, query, search_term):
        m = importlib.import_module(
            'brome.model.{model}'.format(model=self.name.lower())
        )
        model_class = getattr(m, self.name)
        with DbSessionContext(
            BROME_CONFIG['database'].get('mongo_database_name')
                ) as session:
            test_batch_query = session.query(Testbatch)\
                .filter(Testbatch.friendly_name == search_term)
            if test_batch_query.count():
                test_batch = test_batch_query.one()
                query_model = session.query(model_class)\
                    .filter(model_class.test_batch_id == test_batch.get_uid())
                query = query_model.query

        return query


class TestScreenshotForm(form.Form):
    browser_capabilities = DictField()
    browser_id = fields.TextField()
    file_path = fields.TextField()
    root_path = fields.TextField()
    extra_data = DictField()
    title = fields.TextField()

    test_batch_id = fields.SelectField('Test Batch', widget=Select2Widget())


class TestScreenshotView(TestBatchUidToFriendlyNameView):
    column_list = (
        '_id',
        'test_batch_friendly_name',
        'title',
        'created_ts'
    )
    column_sortable_list = (
        '_id',
        'title',
        'created_ts'
    )
    column_searchable_list = ('title')

    form = TestScreenshotForm


class TestInstanceForm(form.Form):
    name = fields.TextField('Name', [validators.DataRequired()])
    browser_capabilities = DictField()
    browser_id = fields.TextField()
    starting_timestamp = fields.DateTimeField()
    ending_timestamp = fields.DateTimeField()
    terminated = fields.BooleanField()
    extra_data = DictField()

    root_path = fields.TextField()
    log_file_path = fields.TextField()
    network_capture_path = fields.TextField()
    video_capture_path = fields.TextField()
    video_location = fields.SelectField(
        choices=[('s3', 's3'), ('local', 'local')]
    )

    test_batch_id = fields.SelectField('Test Batch', widget=Select2Widget())


class TestInstanceView(TestBatchUidToFriendlyNameView):
    column_list = (
        '_id',
        'test_batch_friendly_name',
        'name',
        'created_ts'
    )
    column_sortable_list = (
        '_id',
        'name',
        'created_ts'
    )
    column_searchable_list = ('name')

    form = TestInstanceForm


class TestResultForm(form.Form):
    result = fields.BooleanField()
    browser_capabilities = DictField()
    browser_id = fields.TextField()
    title = fields.TextField()
    testid = fields.TextField()

    root_path = fields.TextField()
    screenshot_path = fields.TextField()
    video_capture_path = fields.TextField()
    video_location = fields.SelectField(
        choices=[('s3', 's3'), ('local', 'local')]
    )
    extra_data = DictField()

    test_batch_id = fields.SelectField('Test Batch', widget=Select2Widget())


class TestResultView(TestBatchUidToFriendlyNameView):
    column_list = (
        '_id',
        'title',
        'testid',
        'test_batch_friendly_name'
    )
    column_sortable_list = (
        '_id',
        'title',
        'testid'
    )
    column_searchable_list = ('testid', 'title')

    form = TestResultForm


class TestForm(form.Form):
    test_id = fields.TextField('Test Id', [validators.DataRequired()])

    name = fields.TextField('Name', [validators.DataRequired()])


class TestView(BaseView):
    column_list = (
        '_id',
        'test_id',
        'name'
    )
    column_sortable_list = (
        '_id',
        'test_id',
        'name'
    )
    column_searchable_list = ('test_id', 'name')

    form = TestForm


class TestCrashForm(form.Form):
    browser_capabilities = DictField('Browser Capabilities')
    browser_id = fields.TextField()

    extra_data = DictField('Extra data')
    trace = fields.TextField()
    title = fields.TextField()

    root_path = fields.TextField()
    screenshot_path = fields.TextField()
    video_capture_path = fields.TextField()
    video_location = fields.SelectField(
        choices=[('s3', 's3'), ('local', 'local')]
    )

    test_batch_id = fields.SelectField('Test Batch', widget=Select2Widget())


class TestCrashView(TestBatchUidToFriendlyNameView):
    column_list = (
        '_id',
        'test_batch_friendly_name',
        'title',
        'created_ts'
    )
    column_sortable_list = (
        '_id',
        'title',
        'created_ts'
    )
    column_searchable_list = ('title')

    form = TestCrashForm


class TestBatchForm(form.Form):
    friendly_name = fields.TextField(
        'Friendly Name',
        [validators.DataRequired()]
    )
    pid = fields.IntegerField()
    killed = fields.BooleanField(default=False)
    total_tests = fields.IntegerField()
    starting_timestamp = fields.DateTimeField(
        'Starting Timestamp',
        [validators.DataRequired()]
    )
    ending_timestamp = fields.DateTimeField('Ending Timestamp')
    terminated = fields.BooleanField('Terminated')
    feature_session_video_capture = fields.BooleanField(
        'Feature Video Capture'
    )
    feature_network_capture = fields.BooleanField('Feature Network Capture')
    # feature_bot_diaries = fields.BooleanField('Feature Bot Diaries')
    feature_screenshots = fields.BooleanField('Feature Screenshots')
    feature_instance_vnc = fields.BooleanField('Feature Instance VNC')
    feature_style_quality = fields.BooleanField('Feature Style Quality')
    runner_metadata = DictField('Runner metadata')
    root_path = fields.TextField('Root path')
    log_file_path = fields.TextField('Log File Path')


class TestBatchView(BaseView):
    column_list = (
        '_id',
        'friendly_name',
        'starting_timestamp',
        'ending_timestamp'
    )
    column_sortable_list = (
        '_id',
        'friendly_name',
        'starting_timestamp',
        'ending_timestamp'
    )
    column_searchable_list = ('friendly_name')

    form = TestBatchForm


class UserForm(form.Form):
    name = fields.TextField('Name', [validators.DataRequired()])
    email = fields.TextField(
        'Email',
        [validators.DataRequired(), validators.Email()]
    )
    role = fields.SelectField(
        'Role',
        choices=[('admin', 'admin'), ('user', 'user')]
    )
    enable = fields.BooleanField('Enable')
    email_confirmed = fields.BooleanField('Email confirmed')
    password = fields.PasswordField('Password')


class UserView(BaseView):
    column_list = ('_id', 'name', 'email', 'role', 'enable', 'email_confirmed')
    column_sortable_list = (
        'name',
        'email',
        'role',
        'enable',
        'email_confirmed'
    )
    column_searchable_list = ('name', 'email')

    form = UserForm


class Admin(object):

    username = config.get('username')
    password = config.get('password')
    role = 'admin'

    def __repr__(self):
        return "Admin"

    def is_authenticated(self):
        # logger.debug('Admin.is_authenticated')
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __unicode__(self):
        return self.username


class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        if self.login.data == config.get('username'):
            return Admin()
        else:
            return None


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == config.get('username'):
            return Admin()
        else:
            return None


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            # logger.debug('not login.current_user.is_authenticated
            # redirect to login_view')
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            # logger.debug('login.current_user.is_authenticated
            # redirect to index')
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


@app.route('/')
def index():
    return redirect(url_for('admin.index'))


init_login()

admin = admin.Admin(
    app,
    'Brome - admin',
    index_view=MyAdminIndexView(),
    base_template='my_master.html'
)
admin.add_view(UserView(db.User, 'User'))
admin.add_view(TestBatchView(db.Testbatch, 'Testbatch'))
admin.add_view(TestInstanceView(db.Testinstance, 'Testinstance'))
admin.add_view(TestCrashView(db.Testcrash, 'Testcrash'))
admin.add_view(TestResultView(db.Testresult, 'Testresult'))
admin.add_view(TestScreenshotView(db.Testscreenshot, 'Testscreenshot'))
admin.add_view(TestView(db.Test, 'Test'))

if __name__ == '__main__':
    host = 'localhost'
    port = 31337
    debug = True
    app.run(host=host, port=port, debug=debug)
