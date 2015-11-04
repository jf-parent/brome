#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, Boolean, Text, Integer, ForeignKey

class TestCrash(SurrogatePK, Base):
    timestamp = Column(DateTime())
    browser_id = Column(Text())
    screenshot_path = Column(Text())
    videocapture_path = Column(Text())
    extra_data = Column(Text())
    trace = Column(Text())
    title = Column(Text())

    test_instance_id = Column(Integer, ForeignKey('testinstance.id'))
    test_batch_id = Column(Integer, ForeignKey('testbatch.id'))
