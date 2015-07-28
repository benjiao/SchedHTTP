#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging
import config
from utilities.daemon import Daemon
from sqlalchemy import create_engine
from tasks import TaskLogic
from tasks import SchedulerHTTPException


class SchedHTTPService(Daemon):
    def setupDaemon(self, config, logger):
        self.config = config
        self.logger = logger

        self.db_engine = create_engine(self.config.DATABASE_URI,
                                       echo=self.config.SQLALCHEMY_ECHO)
        self.tasks = TaskLogic(db_engine=self.db_engine)
        return True

    def start(self):
        logging.info("Sched HTTP Service Started")
        Daemon.start(self)

    def stop(self):
        logging.info("Sched HTTP Service Terminated")
        Daemon.stop(self)

    def run(self):
        while True:
            active_tasks = self.tasks.getActiveTasks()
            self.logger.info("Active Tasks: %s: %s" % (len(active_tasks), str(active_tasks)))

            for task in active_tasks:
                self.logger.info("Task: %s", task.uuid)
                self.logger.info("Retries: %s", task.retry_count)
                try:
                    self.tasks.callTaskHTTPEndpoint(task)
                    self.logger.info("Sent! %s: %s" % (task.uuid, task.endpoint_url))
                except SchedulerHTTPException, e:
                    self.logger.exception("Error: %s", e.value)
                except:
                    self.logger.exception("Error in calling task!")

            time.sleep(self.config.POLL_INTERVAL)

if __name__ == "__main__":
    config = config.Config

    # Setup logging
    logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

    logging.info("PID: %s" % config.DAEMON_PID_FILE)

    daemon = SchedHTTPService(config.DAEMON_PID_FILE,
                              stdout=config.DAEMON_OUT_LOG,
                              stderr=config.DAEMON_ERR_LOG)

    daemon.setupDaemon(
        logger=logging.getLogger("SchedHTTPService"),
        config=config)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
