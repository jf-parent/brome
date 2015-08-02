#!/usr/bin/env python

import sys
import os
from IPython import embed

from brome import Brome

from model.selector import selector_dict
from browser_config.main_config import browsers_config
from model.test_dict import test_dict

if __name__ == '__main__':

    HERE = os.path.abspath(os.path.dirname(__file__))
    brome = Brome(
        config_path = os.path.join(HERE, "brome.ini"),
        selector_dict = selector_dict,
        test_dict = test_dict,
        browsers_config = browsers_config,
        absolute_path = HERE
    )

    brome.execute(sys.argv)

