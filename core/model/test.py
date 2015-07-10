#! -*- coding: utf-8 -*-

from brome.core.model.meta import SurrogatePK, Base, Column, Boolean, Text, relationship

class Test(SurrogatePK, Base):

    test_id = Column(Text())
    name = Column(Text())
    test_results = relationship("TestResult", backref="test")
