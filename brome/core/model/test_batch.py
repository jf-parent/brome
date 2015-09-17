#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, DateTime, relationship, Integer, Boolean

class TestBatch(SurrogatePK, Base):

    pid = Column(Integer())
    killed = Column(Boolean(), default = False)
    total_tests = Column(Integer())
    starting_timestamp = Column(DateTime())
    ending_timestamp = Column(DateTime())
    test_instances = relationship("TestInstance", backref="testbatch")
    test_results = relationship("TestResult", backref="testbatch")
