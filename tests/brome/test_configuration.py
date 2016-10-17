from pytest import set_trace  # noqa

from brome.core.configurator import default_config as brome_default_config
from brome_config import default_config
from brome.core.settings import BROME_CONFIG


def test_default_config(brome):
    for key, value in iter(default_config.items()):
        for sub_key, sub_value in iter(value.items()):
            assert BROME_CONFIG[key][sub_key] == sub_value


def test_default_config_when_config_not_provided(brome):
    brome.configure()

    for key, value in iter(brome_default_config.items()):
        for sub_key, sub_value in iter(value.items()):
            assert BROME_CONFIG[key][sub_key] == sub_value['default']


def test_default_config_when_value_not_provided(brome):
    brome.configure(config={'test': True})

    for key, value in iter(brome_default_config.items()):
        for sub_key, sub_value in iter(value.items()):
            assert BROME_CONFIG[key][sub_key] == sub_value['default']


def test_new_section(brome):
    new_config = default_config.copy()
    new_config['new_section'] = {}
    new_config['new_section']['test'] = 1
    new_config['new_section']['test_1'] = True
    brome.configure(config=new_config)

    assert BROME_CONFIG["new_section"]["test"] == 1
    assert BROME_CONFIG["new_section"]["test_1"]


def test_project_config(brome):
    new_config = default_config.copy()
    new_config['project'] = {}
    new_config['project']['test'] = 1
    new_config['project']['test_1'] = True
    brome.configure(config=new_config)

    assert BROME_CONFIG["project"]["test"] == 1
    assert BROME_CONFIG["project"]["test_1"]


def test_project_absolute_path(brome):
    brome.configure(config={
            'project': {}
        },
        absolute_path="/dev/null/"
    )
    assert BROME_CONFIG["project"]["absolute_path"] == "/dev/null/"
