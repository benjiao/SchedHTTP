from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Task(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True)
    name = Column(String, )