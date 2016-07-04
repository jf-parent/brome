import pytest

from brome import Brome
from brome_config import default_config


@pytest.fixture
def brome():
    brome = Brome(
        config=default_config
    )
    return brome
