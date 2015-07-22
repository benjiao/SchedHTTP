import datetime
import sqlalchemy
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext import mutable


class JsonEncodedDict(sqlalchemy.TypeDecorator):
    impl = sqlalchemy.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    scheduled_time = Column(DateTime)
    endpoint_url = Column(String)
    endpoint_headers = Column(JsonEncodedDict)
    endpoint_body = Column(String)
    endpoint_method = Column(String)
    max_retry_count = Column(Integer)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    sent_date = Column(DateTime, default=None)
    last_retry_date = Column(DateTime, default=None)
    retry_count = Column(Integer, default=0)

    is_sent = Column(Boolean, default=False)
    is_failed = Column(Boolean, default=False)

    def __init__(self, task_uuid, scheduled_time=None,
                 endpoint_url=None, endpoint_headers=None,
                 endpoint_body=None, endpoint_method=None,
                 max_retry_count=None):

        self.uuid = task_uuid
        self.scheduled_time = scheduled_time
        self.endpoint_url = endpoint_url
        self.endpoint_headers = endpoint_headers
        self.endpoint_body = endpoint_body
        self.endpoint_method = endpoint_method
        self.max_retry_count = max_retry_count


if __name__ == '__main__':
    engine = create_engine('sqlite:///db/test.db')
    Base.metadata.create_all(engine)
