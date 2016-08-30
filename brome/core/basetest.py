import logging
import traceback
from time import sleep
import os
import pickle
import urllib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import proxy

from brome.core.settings import BROME_CONFIG
from brome.core.stateful import Stateful
from brome.core.proxy_driver import ProxyDriver
from brome.core.configurator import (
    test_config_to_dict
)
from brome.model.testinstance import Testinstance
from brome.model.testbatch import Testbatch
from brome.model.testresult import Testresult
from brome.model.testcrash import Testcrash
from brome.model.test import Test
from brome.core import exceptions
from brome.core.utils import (
    DbSessionContext,
    utcnow,
    say,
    create_dir_if_doesnt_exist,
    string_to_filename
)


class BaseTest(object):
    """Base test class used to init the driver, load and save state, start and
        stop video recording

    Attributes:
        runner (object): the runner that created the BaseTest instance
        name (str): the name of the test
        index (int): the index of the test
        browser_config (object): the browser config; used to init the driver
        test_batch_id (int): the test batch id
    """

    def __init__(self, runner, name, index, browser_config, test_batch_id, **kwargs):  # noqa
        self._runner = runner
        self._name = name
        self._index = index
        self._browser_config = browser_config
        self._test_batch_id = test_batch_id
        self._localhost_instance = kwargs.get('localhost_instance')
        self._log_file_path = ''

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == test_batch_id)\
                .one()
            self._test_batch_friendly_name = test_batch.friendly_name

        self._crash_error = False

        # TEST BATCH DIRECTORY
        if self._runner.runner_dir:
            self._runner_dir = self._runner.runner_dir
        else:
            self._runner_dir = ''

        # NETWORK CAPTURE
        if self._browser_config.get('enable_proxy'):
            self._network_capture_file_relative_path = os.path.join(
                self._runner.relative_runner_dir,
                'network_capture',
                string_to_filename('%s.data' % self._name)
            )
        else:
            self._network_capture_file_relative_path = ''

        # LOGGING
        self.configure_logger()

        # DRIVER
        self.pdriver = self.init_driver()

        # ASSIGN THE TEST NAME TO THE INSTANCE
        if self._browser_config.location in ['ec2', 'virtualbox']:
            self._runner.resolve_instance_by_ip(
                self.pdriver.get_ip_of_node()
            ).testname = self._name

        # TEST RESULT DIRECTORY
        self.configure_test_result_dir()

        # DRIVER RESOLUTION
        self.pdriver.configure_resolution()

        # VIDEO RECORDING
        self.start_video_recording()
        starting_timestamp = utcnow()

        # TEST KWARGS
        self._test_config = test_config_to_dict(
            BROME_CONFIG['runner'].get('test_config')
        )

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa

            extra_data = {}
            if self._browser_config.location in 'ec2':
                self._private_ip = self.pdriver.get_ip_of_node()
                extra_data['instance_private_ip'] = self._runner.instances_ip[self._private_ip].private_ip  # noqa
                extra_data['instance_public_ip'] = self._runner.instances_ip[self._private_ip].public_ip  # noqa
                extra_data['instance_public_dns'] = self._runner.instances_ip[self._private_ip].public_dns  # noqa
                extra_data['instance_private_dns'] = self._runner.instances_ip[self._private_ip].private_dns  # noqa
            elif self._browser_config.location in 'virtualbox':
                self._private_ip = self._browser_config.get('ip')
                extra_data['instance_private_ip'] = self._private_ip

            capabilities = {
                'browserName': self.pdriver.capabilities['browserName'],
                'platform': self.pdriver.capabilities['platform'],
                'version': self.pdriver.capabilities['version']
            }
            test_instance = Testinstance()
            test_instance.name = self._name
            test_instance.starting_timestamp = starting_timestamp
            test_instance.browser_capabilities = capabilities
            test_instance.browser_id = self.pdriver.get_id()
            test_instance.test_batch_id = self._test_batch_id
            test_instance.extra_data = extra_data
            if self._runner.root_test_result_dir:
                test_instance.log_file_path = self._relative_log_file_path
                test_instance.root_path = self._runner.root_test_result_dir
                test_instance.network_capture_path = self._network_capture_file_relative_path  # noqa
                test_instance.video_capture_path = self._video_capture_file_relative_path  # noqa
            else:
                test_instance.log_file_path = ''
                test_instance.root_path = ''
                test_instance.network_capture_path = ''
                test_instance.video_capture_path = ''

            session.save(test_instance, safe=True)

            self._test_instance_id = test_instance.get_uid()

        # START PROXY
        if self._browser_config.location == 'ec2':
            instance = self._runner.resolve_instance_by_ip(self._private_ip)
            if instance.browser_config.get('enable_proxy'):
                instance.start_proxy()

        # FEATURE DETECTION
        self.detect_feature()

    def detect_feature(self):
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == self._test_batch_id).one()

            # SESSION VIDEO CAPTURE
            if self._browser_config.get('record_session'):
                test_batch.feature_session_video_capture = True

            # NETWORK CAPTURE
            if self._browser_config.get('enable_proxy'):
                test_batch.feature_network_capture = True

            # SCREENSHOT
            if self._runner_dir:
                test_batch.feature_style_quality = True
                test_batch.feature_screenshots = True

            # BOT DIARY
            if BROME_CONFIG['bot_diary']['enable_bot_diary']:
                test_batch.feature_bot_diaries = False

            # TODO VNC

            session.save(test_batch, safe=True)

    def start_video_recording(self):
        self._video_capture_file_relative_path = ''

        # TODO support localhost and more
        if self._browser_config.get('record_session') and \
                self._browser_config.location in ['ec2', 'virtualbox']:
            self.info_log("Starting screen capture...")

            video_capture_file = string_to_filename(
                '%s.mp4' % (self._name.replace(' ', '_'))
            )

            self._video_capture_file_path = os.path.join(
                self._video_recording_dir,
                video_capture_file
            )

            self._video_capture_file_relative_path = os.path.join(
                self._video_recording_relative_dir,
                video_capture_file
            )

            private_ip = self.pdriver.get_ip_of_node()
            instance = self._runner.resolve_instance_by_ip(private_ip)
            instance.start_video_recording(
                self._video_capture_file_path,
                video_capture_file
            )

    def stop_video_recording(self):
        if self._browser_config.get('record_session'):
            self.info_log("Stopping the screen capture...")

            instance = self._runner.resolve_instance_by_ip(self._private_ip)
            instance.stop_video_recording()

    def init_driver(self, retry=30):
        """Init driver will instanciate a webdriver according to the browser config

        First a webdriver is instanciate
            according to the provided browser config
        then the webdriver is wrapped in the brome proxy_driver

        Args:
            retry (int): the number of time the init driver will retry to
                init the driver if it fail
                            default: 10

        Returns:
            proxy_driver instance

        Raises:
            Exception InitDriverException
            Exception InvalidBrowserName

        """

        # LOCAL
        if self._browser_config.location == 'localhost':

            def get_proxy():
                mitm_proxy = "localhost:%s" % self._localhost_instance.proxy_port  # noqa

                return proxy.Proxy({
                    'proxyType': proxy.ProxyType.MANUAL,
                    'httpProxy': mitm_proxy,
                    'sslProxy': mitm_proxy
                })

            # CHROME
            if self._browser_config.get('browserName').lower() == 'chrome':
                chrome_options = webdriver.ChromeOptions()

                if self._browser_config.get('mobile_emulation'):
                    chrome_options.add_experimental_option(
                        "mobileEmulation",
                        self._browser_config.get('mobile_emulation')
                    )
                elif self._browser_config.get('enable_proxy'):
                    chrome_options.add_argument(
                        "--proxy-server={0}".format(get_proxy())
                    )

                driver = webdriver.Chrome(chrome_options=chrome_options)

            elif self._browser_config.get('browserName').lower() \
                    in ['firefox', 'phantomjs'] \
                    and self._browser_config.get('enable_proxy'):

                # NOTE http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#using-a-proxy  # noqa
                # FIREFOX
                if self._browser_config.get('browserName').lower() \
                        == 'firefox':
                    profile = webdriver.FirefoxProfile()
                    profile.set_proxy(proxy=get_proxy())
                    driver = webdriver.Firefox(firefox_profile=profile)

                # PHANTOMJS
                elif self._browser_config.get('browserName').lower() \
                        == 'phantomjs':

                    # TODO investigate why this doesnt work in phantomjs
                    """
                    #WAY 1
                    #http://stackoverflow.com/questions/14699718/how-do-i-set-a-proxy-for-phantomjs-ghostdriver-in-python-webdriver
                    service_args = [
                    '--proxy=127.0.0.1:%s'%self._localhost_instance.proxy_port,
                    '--proxy-type=http',
                    ]
                    driver = webdriver.PhantomJS(service_args=service_args)

                    #WAY 2
                    desired_cap = self._browser_config.config
                    proxy.add_to_capabilities(desired_cap)
                    driver = webdriver.PhantomJS(desired_capabilities = desired_cap) # noqa
                    """
                    raise NotImplemented()

                # NOTE: AFAIK Safari doesn't support proxy
                # https://code.google.com/p/selenium/issues/detail?id=5051
            else:
                try:
                    driver = getattr(
                        webdriver,
                        self._browser_config.get('browserName')
                    )()
                except AttributeError:
                    raise exceptions.InvalidBrowserName(
                        "The browserName('%s') is invalid" %
                        self._browser_config.get('browserName')
                    )

        # APPIUM
        elif self._browser_config.location == 'appium':
            driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723/wd/hub',
                desired_capabilities=self._browser_config.config
            )

        # SAUCELABS
        elif self._browser_config.location == 'saucelabs':
            driver = webdriver.Remote(
                command_executor='http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (  # noqa
                    BROME_CONFIG['saucelabs']['username'],
                    BROME_CONFIG['saucelabs']['key']
                ),
                desired_capabilities=self._browser_config.config
            )

        # BROWSERSTACK
        elif self._browser_config.location == 'browserstack':
            driver = webdriver.Remote(
                command_executor='http://%s:%s@hub.browserstack.com:80/wd/hub' % (  # noqa
                    BROME_CONFIG['browserstack']['username'],
                    BROME_CONFIG['browserstack']['key']
                ),
                desired_capabilities=self._browser_config.config
            )

        # REMOTE
        elif self._browser_config.location in ['virtualbox', 'ec2']:
            config = self._browser_config.config

            desired_cap = {}
            desired_cap['browserName'] = config.get('browserName')
            desired_cap['platform'] = config.get('platform')
            desired_cap['javascriptEnabled'] = True

            if config.get('enable_proxy'):
                mitm_proxy = "localhost:%s" % config.get('proxy_port', 8080)

                _proxy = proxy.Proxy({
                    'proxyType': proxy.ProxyType.MANUAL,
                    'httpProxy': mitm_proxy,
                    'sslProxy': mitm_proxy
                })

            if desired_cap['browserName'].lower() == "chrome":
                chrome_options = Options()
                chrome_options.add_argument("--test-type")
                chrome_options.add_argument("--disable-application-cache")

                if config.get('enable_proxy'):
                    chrome_options.add_argument(
                        '--proxy-server=%s' % mitm_proxy
                    )
                if config.get('mobile_emulation'):
                    chrome_options.add_experimental_option(
                        "mobileEmulation",
                        config.get('mobile_emulation')
                    )

                desired_cap = chrome_options.to_capabilities()

            try:
                command_executor = "http://%s:%s/wd/hub" % (  # noqa
                    BROME_CONFIG['grid_runner']['selenium_server_ip'],
                    BROME_CONFIG['grid_runner']['selenium_server_port']
                )

                if desired_cap['browserName'].lower() == "firefox" \
                        and config.get('enable_proxy'):
                    profile = webdriver.FirefoxProfile()
                    profile.set_proxy(proxy=_proxy)
                    driver = webdriver.Remote(
                            browser_profile=profile,
                            desired_capabilities=desired_cap,
                            command_executor=command_executor)
                else:
                    driver = webdriver.Remote(
                            command_executor=command_executor,
                            desired_capabilities=desired_cap
                    )

                self.info_log('Got a session')

            except Exception as e:
                if str(e).find("Error forwarding the new session") != -1:
                    if retry:

                        self.info_log("Waiting 5 sec because the pool doesn't contain the needed browser.")  # noqa

                        sleep(5)

                        return self.init_driver(retry=(retry - 1))
                    else:
                        raise exceptions.InitDriverException("Cannot get the driver")  # noqa

        # Wrap the driver in the brome proxy driver and return it
        return ProxyDriver(
            driver=driver,
            test_instance=self,
            runner=self._runner
        )

    def delete_state(self, state_pickle=None):
        """This will delete the pickle that hold the saved test state

        Args:
            state_pickle (path): the path of the pickle that will be delete
        """
        if not state_pickle:
            state_pickle = self.get_state_pickle_path()

        if os.path.isfile(state_pickle):
            os.remove(state_pickle)
            self.info_log("State deleted: %s" % state_pickle)

    def get_state_pickle_path(self):
        """Return the state's pickle path

        The project:url config need to be set in order to
            extract the server name. Each server will have it own state
        The test name is used to name the state.

        E.g.: the test named "test 1" that run with the project:url
            ("http://www.example.com") with have a state named:
        tests/states/test_1_example.com.pkl

        Returns: str (path)
        """

        # Extract the server name
        server = urllib.parse.urlparse(
            BROME_CONFIG['project']['url']
        ).netloc

        if BROME_CONFIG['project']['test_batch_result_path']:
            states_dir = os.path.join(
                BROME_CONFIG['project']['absolute_path'],
                BROME_CONFIG['project']['script_folder_name'],
                "states"
            )
            create_dir_if_doesnt_exist(states_dir)

            # TODO should be configurable
            state_pickle_path = os.path.join(
                states_dir,
                string_to_filename(
                    '%s_%s.pkl' %
                    (
                        self._name.replace(' ', '_'),
                        server
                    )
                )
            )

            return state_pickle_path
        else:
            return False

    def save_state(self):
        """Save the state in a pickle

        First remove all the instance variables that are private (_*).
        Then remove the pdriver instance variable.
        Finally cleanup the state using the Stateful.cleanup_state function.
        The cleanup is recursive.

        The test state will be saved to the path returned by the
            get_state_pickle_path.

        Returns: None
        """
        self.info_log("Saving state...")

        state = {}

        # Remove all the instance variables that are private
        state = {key: value for (key, value) in iter(self.__dict__.items()) if key[0] != '_'}  # noqa

        # Remove the pdriver
        del state['pdriver']

        # Cleanup the state
        effective_state = Stateful.cleanup_state(state)

        # Save the state
        state_pickle_path = self.get_state_pickle_path()
        if state_pickle_path:
            with open(state_pickle_path, 'wb') as fd:
                pickle.dump(effective_state, fd)

            self.info_log("State saved: %s" % state_pickle_path)

    def load_state(self):
        """Load the state pickle into the instance object if a state is found

        The state will be loaded in the basetest instance if a state exist.
        The pdriver will be set on each instance that inherited from Stateful
        These instance can be in a dict or a list. It is not recursive tho.

        If the instance has an after_load method, this method will be called
        E.g.:
        class Base(object):
            def after_load(self):
                self.app = self.pdriver.app

        Returns: bool True if a state was found; False if no state was found;
        """
        self.info_log("Loading state...")

        # Set the pdriver for an object that inherited from Stateful
        def set_pdriver(value):
            # TODO support class that inherited Stateful
            if Stateful in value.__class__.__bases__:
                value.pdriver = self.pdriver
                if hasattr(value, 'after_load'):
                    value.after_load()
            elif type(value) is list:
                for v in value:
                    set_pdriver(v)
            elif type(value) is dict:
                for k, v in iter(value.items()):
                    set_pdriver(v)

        # Load the state pickle
        state_pickle_path = self.get_state_pickle_path()
        if state_pickle_path:
            if os.path.isfile(state_pickle_path):
                with open(state_pickle_path, 'rb') as fd:
                    state = pickle.load(fd)
            else:
                self.info_log("No state found.")

                return False
        else:
            self.info_log("No state found.")
            return False

        # Set the pdriver
        for key, value in iter(state.items()):
            set_pdriver(value)

        # Update the instance variable dictionary
        self.__dict__.update(state)

        self.info_log("State loaded.")

        return True

    def configure_logger(self):
        """Configure the logger for the test

        Configure the logger from the logger_test config:
            logger_test:level
            logger_test:streamlogger
            logger_test:filelogger
            logger_test:format

        See documentation: http://brome.readthedocs.org/en/release/configuration.html#logger-test  # noqa

        If the config project:test_batch_result_path is set to False then the
            filelogger will not be configured.

        Returns: None
        """

        # Logger name
        logger_name = self._name

        # Log directory
        if self._runner_dir:
            self._test_log_dir = os.path.join(
                self._runner_dir,
                "logs"
            )
            self._relative_test_log_dir = os.path.join(
                self._runner.relative_runner_dir,
                "logs"
            )
        else:
            self._test_log_dir = ''
            self._relative_test_log_dir = ''

        # Logger
        self._logger = logging.getLogger(logger_name)

        # Create the log directory
        if self._runner_dir:
            create_dir_if_doesnt_exist(self._test_log_dir)

        # Format
        format_ = BROME_CONFIG['logger_test']['format']

        # Stream logger
        if BROME_CONFIG['logger_test']['streamlogger']:
            sh = logging.StreamHandler()
            stream_formatter = logging.Formatter(format_)
            sh.setFormatter(stream_formatter)
            self._logger.addHandler(sh)

        # File logger
        if self._runner_dir:
            if BROME_CONFIG['logger_test']['filelogger']:
                test_name = string_to_filename(self._name)
                self._log_file_path = os.path.join(
                    self._test_log_dir,
                    "%s_%s.log" %
                    (test_name, self._browser_config.get('browserName'))
                )
                self._relative_log_file_path = os.path.join(
                    self._relative_test_log_dir,
                    "%s_%s.log" %
                    (test_name, self._browser_config.get('browserName'))
                )
                fh = logging.FileHandler(
                    self._log_file_path
                )
                file_formatter = logging.Formatter(format_)
                fh.setFormatter(file_formatter)
                self._logger.addHandler(fh)

        # Set level
        self._logger.setLevel(getattr(
            logging, BROME_CONFIG['logger_test']['level'])
        )

    def get_logger_dict(self):
        return {
            'batchid': self._test_batch_friendly_name,
            'testname': u"%s" % self._name
        }

    def debug_log(self, msg):
        self._logger.debug(u"[debug]%s" % msg, extra=self.get_logger_dict())

    def info_log(self, msg):
        self._logger.info(u"%s" % msg, extra=self.get_logger_dict())

    def warning_log(self, msg):
        self._logger.warning(
            u"[warning]%s" % msg,
            extra=self.get_logger_dict()
        )

    def error_log(self, msg):
        self._logger.error(u"[error]%s" % msg, extra=self.get_logger_dict())

    def critical_log(self, msg):
        self._logger.critical(
            u"[critical]%s" % msg,
            extra=self.get_logger_dict()
        )

    def execute(self):
        try:
            self.before_run()

            if self._test_config.get("delete_state"):
                state_pickle_path = self.get_state_pickle_path()
                if state_pickle_path:
                    self.delete_state(state_pickle_path)
                else:
                    self.info_log('No state to delete!')

            if not self.load_state():
                if hasattr(self, 'create_state'):
                    ret = self.create_state()
                    if ret:
                        self.save_state()

            self.run(**self._test_config)

            self.after_run()

        except Exception as e:
            self.error_log('Test failed')

            tb = traceback.format_exc()

            self.error_log('Crash: %s' % tb)

            self.fail(tb)
        finally:
            self.end()

    def end(self):
        self.info_log("Test ended")

        # STOP PROXY
        if self._browser_config.location == 'ec2':
            instance = self._runner.resolve_instance_by_ip(self._private_ip)
            if instance.browser_config.get('enable_proxy'):
                instance.stop_proxy()

        self.stop_video_recording()
        ending_timestamp = utcnow()

        self.quit_driver()

        if BROME_CONFIG['runner']['play_sound_on_test_finished']:
            say(BROME_CONFIG['runner']['sound_on_test_finished'])

        ending_timestamp = ending_timestamp
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_instance = session.query(Testinstance)\
                .filter(Testinstance.mongo_id == self._test_instance_id).one()
            test_instance.ending_timestamp = ending_timestamp
            test_instance.terminated = True
            session.save(test_instance, safe=True)

        self.info_log("Ending timestamp: %s" % ending_timestamp)

    def quit_driver(self):
        self.info_log("Quitting the browser...")
        try:
            self.pdriver.quit()
        except Exception as e:
            self.error_log('Exception driver.quit(): %s' % str(e))

        """
        if hasattr(self, 'browsermobserver'):
            with open("temp.har", "w") as fd:
                fd.write(json.dumps(self.proxy.har))

            self.browsermobserver.stop()
        """

    def before_run(self):
        pass

    def after_run(self):
        pass

    def fail(self, tb):
        if BROME_CONFIG['runner']['play_sound_on_test_crash']:
            say(BROME_CONFIG['runner']['sound_on_test_crash'])

        if BROME_CONFIG['runner']['embed_on_test_crash']:
            self.pdriver.embed()

        if self.pdriver.bot_diary:
            if not self.pdriver.bot_diary.is_empty():
                traceback = tb
                tb = '\nBot Diary:\n'
                tb += self.pdriver.bot_diary.get_section(-1)[-1] + '\n'
                tb += 'And it failed\n'
                tb += str(traceback)

        self._crash_error = '[!]%s %s crashed: %s' % (self._name, self._browser_config.get_id(), str(tb))  # noqa

        self.create_crash_report(tb)

    def create_crash_report(self, tb):
        self.info_log('Creating a crash report')

        crash_name = "%s - %s" % (self.pdriver.get_id(join_char=' ', browser_version_join_char='.'), self._name)  # noqa

        extra_data = {}

        # JAVASCRIPT ERROR
        extra_data['javascript_error'] = self.pdriver.get_javascript_error()

        crash_screenshot_relative_path = ''
        if self._runner_dir:
            crash_screenshot_path = os.path.join(
                self._crash_report_dir,
                string_to_filename('%s.png' % crash_name)
            )

            crash_screenshot_relative_path = os.path.join(
                self._crash_report_relative_dir,
                string_to_filename('%s.png' % crash_name)
            )

            # CRASH LOG
            with open(os.path.join(self._crash_report_dir, string_to_filename('%s.log' % crash_name)), 'w') as f:  # noqa
                f.write(str(tb))

            # CRASH SCREENSHOT
            self.pdriver.take_screenshot(screenshot_path=crash_screenshot_path)

        # CRASH OBJECT
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            capabilities = {
                'browserName': self.pdriver.capabilities['browserName'],
                'platform': self.pdriver.capabilities['platform'],
                'version': self.pdriver.capabilities['version']
            }
            test_crash = Testcrash()
            test_crash.title = self._name
            test_crash.browser_capabilities = capabilities
            test_crash.browser_id = self.pdriver.get_id()
            test_crash.timestamp = utcnow()
            test_crash.trace = str(tb)
            if self._runner.root_test_result_dir:
                test_crash.root_path = self._runner.root_test_result_dir
                test_crash.screenshot_path = crash_screenshot_relative_path
                test_crash.video_capture_path = self._video_capture_file_relative_path  # noqa
            else:
                test_crash.root_path = ''
                test_crash.screenshot_path = ''
                test_crash.video_capture_path = ''
            test_crash.extra_data = extra_data
            test_crash.test_instance_id = self._test_instance_id
            test_crash.test_batch_id = self._test_batch_id

            session.save(test_crash, safe=True)

    def configure_test_result_dir(self):

        if not self._runner_dir:
            return

        # CRASH DIRECTORY
        self._crash_report_dir = os.path.join(
            self._runner_dir,
            'crashes'
        )
        create_dir_if_doesnt_exist(self._crash_report_dir)

        self._crash_report_relative_dir = os.path.join(
            self._runner.relative_runner_dir,
            'crashes'
        )

        # ASSERTION SCREENSHOT DIRECTORY
        self._assertion_screenshot_relative_dir = os.path.join(
            self._runner.relative_runner_dir,
            'assertion_screenshots',
            self.pdriver.get_id(join_char='_')
        )

        self._assertion_screenshot_dir = os.path.join(
            self._runner_dir,
            'assertion_screenshots',
            self.pdriver.get_id(join_char='_')
        )
        create_dir_if_doesnt_exist(self._assertion_screenshot_dir)

        # SCREENSHOT DIRECTORY
        self._screenshot_relative_dir = os.path.join(
            self._runner.relative_runner_dir,
            'screenshots',
            self.pdriver.get_id(join_char='_')
        )

        self._screenshot_dir = os.path.join(
            self._runner_dir,
            'screenshots',
            self.pdriver.get_id(join_char='_')
        )
        create_dir_if_doesnt_exist(self._screenshot_dir)

        # QUALITY SCREENSHOT DIRECTORY
        self._quality_screenshot_relative_dir = os.path.join(
            self._runner.relative_runner_dir,
            'quality_screenshots',
            self.pdriver.get_id(join_char='_')
        )

        self._quality_screenshot_dir = os.path.join(
            self._runner_dir,
            'quality_screenshots',
            self.pdriver.get_id(join_char='_')
        )
        create_dir_if_doesnt_exist(self._quality_screenshot_dir)

        # VIDEO RECORDING DIRECTORY
        if self._browser_config.get('record_session'):
            self._video_recording_dir = os.path.join(
                self._runner_dir,
                'video_recording',
                self.pdriver.get_id(join_char='_')
            )
            create_dir_if_doesnt_exist(self._video_recording_dir)

            self._video_recording_relative_dir = os.path.join(
                self._runner.relative_runner_dir,
                'video_recording',
                self.pdriver.get_id(join_char='_')
            )

        # NETWORK CAPTURE DIRECTORY
        if self._browser_config.get('enable_proxy'):
            self._network_capture_dir = os.path.join(
                self._runner_dir,
                'network_capture'
            )
            create_dir_if_doesnt_exist(self._network_capture_dir)

    def get_test_result_summary(self):
        results = []

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            base_query = session.query(Testresult).filter(Testresult.test_instance_id == self._test_instance_id).filter(Testresult.browser_id == self.pdriver.get_id())  # noqa
            total_test = base_query.count()
            total_test_successful = base_query.filter(Testresult.result == True).count()  # noqa
            base_query = session.query(Testresult).filter(Testresult.test_instance_id == self._test_instance_id).filter(Testresult.browser_id == self.pdriver.get_id())  # noqa
            total_test_failed = base_query.filter(Testresult.result == False).count()  # noqa
            base_query = session.query(Testresult)\
                .filter(Testresult.test_instance_id == self._test_instance_id)\
                .filter(Testresult.browser_id == self.pdriver.get_id())
            failed_tests = base_query.filter(Testresult.result == False).all()  # noqa

            results.append('Total_test: %s; Total_test_successful: %s; Total_test_failed: %s' % (total_test, total_test_successful, total_test_failed))  # noqa

            failed_tests_title = []
            for failed_test in failed_tests:
                if failed_test.title not in failed_tests_title:
                    failed_tests_title.append(failed_test.title)
                    query = session.query(Test)\
                        .filter(Test.mongo_id == failed_test.test_id)
                    if query.count():
                        test = query.one()
                        test_id = test.test_id
                    else:
                        test_id = 'n/a'

                    results.append('[%s] %s' % (test_id, failed_test.title))

        return results
