#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, Boolean, Text, Integer, ForeignKey

class TestResult(SurrogatePK, Base):
    result = Column(Boolean())
    timestamp = Column(DateTime())
    browser_id = Column(Text())
    screenshot_path = Column(Text())
    videocapture_path = Column(Text())
    extra_data = Column(Text())
    title = Column(Text())

    test_id = Column(Integer, ForeignKey('test.id'))
    test_instance_id = Column(Integer, ForeignKey('testinstance.id'))
    test_batch_id = Column(Integer, ForeignKey('testbatch.id'))
