from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import engine_from_config, MetaData, create_engine
from decorator import decorator

from brome.core.model import *
from brome.core.model.meta import MultipleResultsFound

engine = None

@decorator
def commit_on_success(fn, *args, **kwargs):
    """Decorate any function to commit the session on success, rollback in
    the case of error."""

    try:
        result = fn(*args, **kwargs)
        Session.commit()
    except:
        Session.rollback()
        raise
    else:
        return result

Session = scoped_session(sessionmaker())

class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=Base)

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
#
Base.metadata.naming_convention={
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s"
    }

def delete_database(sqlalchemy_url, db_name):
    engine = create_engine('/'.join(sqlalchemy_url.split('/')[:-1]))
    conn = engine.connect()
    conn.execute("DROP DATABASE IF EXISTS %s"%db_name)
    conn.close()

def create_database(sqlalchemy_url, db_name):
    engine = create_engine('/'.join(sqlalchemy_url.split('/')[:-1]))
    conn = engine.connect()
    conn.execute("CREATE DATABASE %s"%db_name)
    conn.close()

def setup_database(config):
    """Setup the application given a config dictionary."""

    global engine
    global Base
    engine = engine_from_config(config, "sqlalchemy.")
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

def update_test(session, test_dict):
    from brome.core.model.test import Test
    for test_id, test_config in test_dict.iteritems():
        if type(test_config) == dict:
            name = test_config['name']
        else:
            name = test_config

        #NEW TEST
        if not session.query(Test).filter(Test.test_id == test_id).count():
            test = Test(test_id = test_id, name = name)
            session.add(test)
            print 'Added test id', test_id
        #UPDATE TEST
        else:
            test = session.query(Test).filter(Test.test_id == test_id).one()
            if test.name != name:
                unittest.name = name
                print 'Updated test id', test_id

    session.commit()
