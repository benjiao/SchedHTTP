import logging
from sqlalchemy.pool import NullPool


class Config(object):
    DEBUG = True

    LOG_FILE = '/var/log/schedhttp/schedhttp-api.log'
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    LOG_LEVEL = logging.DEBUG

    DAEMON_PID_FILE = '/tmp/schedhttp-service.pid'
    DAEMON_OUT_LOG = '/var/log/schedhttp/schedhttp-service.out.log'
    DAEMON_ERR_LOG = '/var/log/schedhttp/schedhttp-service.err.log'

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOLCLASS = NullPool
    DATABASE_URI = 'sqlite:///db/app.db'
    TEST_DATABASE_URI = 'sqlite:///db/test.db'

    """
    Sample config for MySQL Setup
    """
    # SQLALCHEMY_POOLCLASS = None
    # DATABASE_URI = 'mysql://root:password@localhost/schedulerdb'
    # TEST_DATABASE_URI = 'mysql://root:password@localhost/schedulertestdb'

    """
    The number of seconds between each check
    """
    POLL_INTERVAL = 5
