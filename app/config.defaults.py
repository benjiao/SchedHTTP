import logging


class Config(object):
    LOG_FILE = 'tmp/scheduler.log'
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
    LOG_LEVEL = logging.DEBUG

    DAEMON_PID_FILE = '/tmp/schedhttp-service.pid'
    DAEMON_OUT_LOG = '/var/log/schedhttp/schedhttp-service.out.log'
    DAEMON_ERR_LOG = '/var/log/schedhttp/schedhttp-service.err.log'

    SQLALCHEMY_ECHO = False
    DATABASE_URI = 'sqlite:///db/app.db'
    TEST_DATABASE_URI = 'sqlite:///db/test.db'

    """
    The number of seconds between each check
    """
    POLL_INTERVAL = 5
