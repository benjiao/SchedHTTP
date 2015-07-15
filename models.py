from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine


Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    scheduled_time = Column(Integer)
    endpoint_url = Column(String)
    endpoint_headers = Column(String)
    endpoint_body = Column(String)
    endpoint_method = Column(String)
    retry_count = Column(Integer)
    last_retry_date = Column(Integer)
    tags = Column(String)
    flags = Column(Integer)
    max_retry_count = Column(Integer)

if __name__ == '__main__':
    engine = create_engine('sqlite:///app.db')
    Base.metadata.create_all(engine)
