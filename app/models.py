import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    scheduled_time = Column(Integer)
    endpoint_url = Column(String)
    endpoint_headers = Column(String)
    endpoint_body = Column(String)
    endpoint_method = Column(String)
    max_retry_count = Column(Integer)

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_retry_date = Column(DateTime, default=None)
    retry_count = Column(Integer, default=0)

    def __init__(self, task_uuid, scheduled_time=None,
                 endpoint_url=None, endpoint_headers=None,
                 endpoint_body=None, endpoint_method=None,
                 retry_count=None, last_retry_date=None,
                 max_retry_count=None):

        self.uuid = task_uuid
        self.scheduled_time = scheduled_time
        self.endpoint_url = endpoint_url
        self.endpoint_headers = endpoint_headers
        self.endpoint_body = endpoint_body
        self.endpoint_method = endpoint_method
        self.retry_count = retry_count
        self.last_retry_date = last_retry_date
        self.max_retry_count = max_retry_count


if __name__ == '__main__':
    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine)
