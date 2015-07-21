import logging


class Config(object):
    LOG_FILE = 'tmp/scheduler.log'
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    LOG_LEVEL = logging.DEBUG

    DATABASE_URI = 'sqlite:///db/app.db'
    TEST_DATABASE_URI = 'sqlite:///db/test.db'
