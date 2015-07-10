#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Text, Base, Column, DateTime, ForeignKey, Integer, relationship

class TestInstance(SurrogatePK, Base):

    name = Column(Text())

    starting_timestamp = Column(DateTime())
    ending_timestamp = Column(DateTime())

    test_batch_id = Column(Integer, ForeignKey('testbatch.id'))
    test_results = relationship("TestResult", backref="testinstance")
