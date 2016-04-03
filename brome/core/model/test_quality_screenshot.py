#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, Boolean, Text, Integer, ForeignKey

class TestQualityScreenshot(SurrogatePK, Base):
    timestamp = Column(DateTime())
    browser_id = Column(Text())
    screenshot_path = Column(Text())
    extra_data = Column(Text())
    title = Column(Text())

    test_instance_id = Column(Integer, ForeignKey('testinstance.id'))
    test_batch_id = Column(Integer, ForeignKey('testbatch.id'))
