#! -*- coding: utf-8 -*-

import logging

from brome.core.model.utils import *
from brome.core.model.selector import Selector

class BotDiary(object):

    def __init__(self, pdriver):
        self.pdriver = pdriver
        self.sections = []
        self.section_index = -1
        self.entry_id = 0

        self.auto_diary = self.pdriver.get_config_value("bot_diary:enable_auto_bot_diary")

        self.configure_logger()

        self.add_section()

    def configure_logger(self):
        #Logger name
        logger_name = 'Bot Diary %s'%self.pdriver.test_instance._name

        #Log directory
        if self.pdriver.test_instance._runner_dir:
            self.bot_diary_dir = os.path.join(
                self.pdriver.test_instance._runner_dir,
                "bot_diary"
            )

            self.nodes_dir = os.path.join(
                self.pdriver.test_instance._runner_dir,
                "bot_diary",
                string_to_filename(self.pdriver.test_instance._name)
            )

            #Create the bot diary directory
            create_dir_if_doesnt_exist(self.bot_diary_dir)
            #Create the nodes screenshot directory
            create_dir_if_doesnt_exist(self.nodes_dir)

        #Logger
        self._logger = logging.getLogger(logger_name)

        #Stream logger 
        if self.pdriver.get_config_value('bot_diary:streamlogger'):
            sh = logging.StreamHandler()
            self._logger.addHandler(sh)

        #File logger
        if self.pdriver.test_instance._runner_dir:
            if self.pdriver.get_config_value('bot_diary:filelogger'):
                test_name = string_to_filename(self.pdriver.test_instance._name)
                fh = logging.FileHandler(os.path.join(
                    self.bot_diary_dir,
                    "%s.log"%test_name
                ))
                self._logger.addHandler(fh)

        self._logger.setLevel("INFO")

    def gen_next_entry_id(self):
        self.entry_id += 1

    def add_section(self):
        self.sections.append([])
        self.section_index += 1
        self._logger.info("[%d] ===%d==="%(self.get_next_entry_id(), self.section_index))
        self.gen_next_entry_id()

    def add_entry(self, entry):
        formatted_entry = "[%d] %s"%(self.get_next_entry_id(), entry)
        self._logger.info("%s"%formatted_entry)
        self.sections[self.section_index].append(formatted_entry)
        self.gen_next_entry_id()

    def add_auto_entry(self, action, **kwargs):
        """

        Keyword arguments:
            selector (str): default: false
            target (str): default: false
            take_screenshot (bool): default: false
        """

        selector = kwargs.get('selector', False)
        target = kwargs.get('target', False)
        take_screenshot = kwargs.get('take_screenshot', False)

        if target:
            effective_target = target
        elif selector:
            _selector = Selector(self.pdriver, selector)
            effective_target =  _selector.get_human_readable()
        else:
            effective_target = ""

        text_dict = {
            'action': action,
            'target': effective_target
        }

        if self.pdriver.get_config_value("bot_diary:enable_auto_bot_diary_component_screenshot") \
            and selector:
            self.pdriver.take_node_screenshot(
                self.pdriver.find(selector),
                os.path.join(self.nodes_dir, "%s.png"%self.get_next_entry_id())
            )
        elif take_screenshot:
            self.pdriver.take_screenshot(screenshot_path = os.path.join(self.nodes_dir, "%s.png"%self.get_next_entry_id()))

        if self.is_auto_diary_active():
            self.add_entry("{action} {target}.".format(**text_dict))
            return True
        else:
            return False

    def print_diary(self):
        for i, section in enumerate(self.sections):
            print 'Section %d'%i
            for entry in section:
                print entry

################################################################################ 
# IS
################################################################################ 

    def is_auto_diary_active(self):
        return self.auto_diary

    def is_empty(self):
        return self.sections[0] == []

################################################################################ 
# SET
################################################################################ 

    def set_enable_auto_diary(self):
        self.auto_diary = True

    def set_disable_auto_diary(self):
        self.auto_diary = False

    def set_section_index(self, index):
        self.section_index = index

################################################################################ 
# GET
################################################################################ 

    def get_next_entry_id(self):
        return self.entry_id + 1

    def get_section(self, index, join = False):
        if join:
            return '\n'.join(self.sections[index])
        else:
            return self.sections[index]

    def get_sections(self):
        return self.sections
