import copy

import pytest

from brome.core.exceptions import BromeBrowserConfigException
from brome.model.testbatch import Testbatch
from brome.core.settings import BROME_CONFIG
from brome_config import default_config
from model.basetest import BaseTest
from model.selector import selector_dict
from model.test_dict import test_dict
from brome.runner.grid_runner import GridRunner
from brome.core.utils import DbSessionContext
from brome.model.testcrash import Testcrash


BROWSERS_DICT = {
    'dummy': {
        'amiid': 'DUMMY',
        'browserName': 'dummy',
        'hub_ip': '127.0.0.1',
        'platform': 'LINUX',
        'launch': True,
        'ssh_key_path': '/path/to/identity.pem',
        'terminate': True,
        'nb_browser_by_instance': 1,
        'max_number_of_instance': 30,
        'username': 'ubuntu',
        'window_height': 950,
        'window_width': 1550,
        'region': 'us-east-1',
        'security_group_ids': ['sg-DUMMY'],
        'instance_type': 't2.micro',
        'selenium_command': 'dummy'
    }
}


class TestGridRunner(object):
    class Test(BaseTest):
        name = 'Grid Runner Test'

        def run(self, **kwargs):

            self.info_log("Running...")


def test_grid_runner_ec2_config_validation(
        brome,
        selenium_monkeypath,
        ec2_instance_monkeypath):
    brome_config = default_config.copy()
    brome_config['runner_args']['remote_runner'] = 'dummy'
    brome_config['grid_runner']['start_selenium_server'] = False

    def reconfigure(browsers_dict):
        brome.configure(
            config=brome_config,
            selector_dict=selector_dict,
            test_dict=test_dict,
            browsers_config=browsers_dict,
            tests=[TestGridRunner]
        )

    essential_keys = [
        'browserName',
        'platform',
        'ssh_key_path',
        'username',
        'region',
        'instance_type',
        'security_group_ids',
        'selenium_command'
    ]
    for key in essential_keys:
        with pytest.raises(BromeBrowserConfigException):
            browsers_dict = copy.deepcopy(BROWSERS_DICT)
            del browsers_dict['dummy'][key]
            reconfigure(browsers_dict)

            GridRunner(brome).execute()
            assert False

    non_essential_keys = [
        'window_width'
    ]
    for key in non_essential_keys:
        browsers_dict = copy.deepcopy(BROWSERS_DICT)
        del browsers_dict['dummy'][key]
        reconfigure(browsers_dict)

        GridRunner(brome).execute()


def test_grid_runner_ec2_success(
        brome,
        selenium_monkeypath,
        ec2_instance_monkeypath):

    NB_TESTS = 10
    browsers_dict = copy.deepcopy(BROWSERS_DICT)

    brome_config = default_config.copy()
    brome_config['runner_args']['remote_runner'] = 'dummy'
    brome_config['grid_runner']['start_selenium_server'] = False
    brome_config['logger_runner']['streamlogger'] = False
    brome_config['logger_test']['streamlogger'] = False

    brome.configure(
        config=brome_config,
        selector_dict=selector_dict,
        test_dict=test_dict,
        browsers_config=browsers_dict,
        tests=[TestGridRunner]*NB_TESTS
    )

    # SUCCESS
    grid_runner = GridRunner(brome)
    grid_runner.execute()

    assert len(grid_runner.instances['dummy']) == NB_TESTS
    test_batch_id = grid_runner.test_batch_id

    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
        assert not session.query(Testcrash)\
            .filter(Testcrash.test_batch_id == test_batch_id).count()

        test_batch = session.query(Testbatch)\
            .filter(Testbatch.mongo_id == test_batch_id)\
            .one()

        runner_metadata = test_batch.runner_metadata
        assert 'InstanceSetupCompleted' in runner_metadata['milestones'].keys()
        assert runner_metadata['milestones']['NbInstanceToSetup']['values']['nb'] == NB_TESTS  # noqa
        assert 'InstanceTearDownCompleted' in runner_metadata['milestones'].keys()  # noqa
