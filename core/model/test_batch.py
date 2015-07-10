#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, relationship

class TestBatch(SurrogatePK, Base):

    starting_timestamp = Column(DateTime())
    ending_timestamp = Column(DateTime())
    test_instances = relationship("TestInstance", backref="testbatch")
    test_results = relationship("TestResult", backref="testbatch")
