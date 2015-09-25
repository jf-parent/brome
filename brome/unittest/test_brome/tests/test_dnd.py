#! -*- coding: utf-8 -*-

from brome.core.model.utils import *

from model.basetest import BaseTest

class Test(BaseTest):

    name = 'Drag and Drop'

    def run(self, **kwargs):

        self.info_log("Running...")

        self.app.pdriver.get("http://touchpunch.furf.com/content.php?/droppable/default-functionality")

        self.app.pdriver.drag_and_drop(
            "id:draggable",
            "id:droppable"
        )

        self.app.pdriver.assert_visible("xp://p[contains(text(), 'Dropped!')]", "Dnd test")

        """
        self.app.go_to("dnd_test")

        self.app.pdriver.drag_and_drop(
            "id:column-a",
            "id:column-b"
        )

        els = self.app.pdriver.find_all("cn:column")
        assert els[0].get_attribute('id') == "column-b"
        """
