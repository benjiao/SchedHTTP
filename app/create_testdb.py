"""
This script initializes a new DB for the app
"""

import config
from sqlalchemy import create_engine
from models import Base

config = config.Config()
engine = create_engine(config.TEST_DATABASE_URI)
Base.metadata.create_all(engine)
