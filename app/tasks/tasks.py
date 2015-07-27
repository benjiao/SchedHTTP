import uuid
import urllib2
import httplib
import logging
from models import Task
from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import sessionmaker
from utilities.request2 import Request2

from exceptions import SchedulerHTTPException


class TaskLogic:
    def __init__(self, db_engine):
        self.logger = logging.getLogger("TaskLogic")
        self.engine = db_engine
        self.sm = sessionmaker(bind=self.engine)

    def createTask(self, scheduled_time, endpoint_url,
                   endpoint_headers, endpoint_body,
                   endpoint_method="GET", max_retry_count=5):
        """ This function inserts a new Task into the database

            :param scheduled_time: The set timestamp when the task is going to be run
            :type scheduled_time: datetime.

            :param endpoint_url: The URL to be called when on the scheduled time indicated
            :type endpoint_url: str -- A valid URL string

            :param endpoint_headers: The headers to include in the scheduled API call
            :type endpoint_headers: dict.

            :param endpoint_body: The body to include in the scheduled API call
            :type endpoint_body: str.

            :param endpoint_method: The method to use for the scheduled API call
            :type endpoint_method: str -- Must be a valid http method

            :param max_retry_count: When a scheduled API call fails, the scheduler attempts to call again
                                    until max_retry_count is reached
            :type max_retry_count: int.

            :return: A hash used to identify the task created
            :rtype: str -- A UUID string
        """

        task_uuid = str(uuid.uuid4())

        newtask = Task(
            task_uuid=task_uuid,
            scheduled_time=scheduled_time,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            endpoint_body=endpoint_body,
            endpoint_method=endpoint_method,
            max_retry_count=max_retry_count)

        session = self.sm()
        try:
            session.add(newtask)
            session.commit()
        except:
            raise
        finally:
            session.close()

        return task_uuid

    def getTaskByUUID(self, task_uuid):
        """ Retrieves a specific Task using its UUID

            :param task_uuid: The task's UUID returned upon creation
            :type task_uuid: str -- A UUID string

            :retrun: The task
            :rtype: A Task object
        """

        session = self.sm()
        try:
            results = session.query(Task).filter_by(uuid=task_uuid).limit(1)
        except:
            raise
        finally:
            session.close()

        return results.first()

    def deleteTaskByUUID(self, task_uuid):
        """ Deletes a task using its UUID

            :param task_uuid: The UUID of the task to be deleted
            :type task_uuid: str -- A UUID string

            :return: True if successful, False otherwise
            :rtype: boolean
        """

        session = self.sm()
        try:
            session.query(Task).filter_by(uuid=task_uuid).\
                delete(synchronize_session=False)
            session.commit()
        except:
            raise
        finally:
            session.close()

        return True

    def getTaskCount(self, include_done=True):
        """ Retrieves the number of tasks currently in the DB

            :param include_done: Controls whether or not to include finished tasks in the count
            :type include_done: boolean

            :return: The number of tasks in the DB
            :rtype: int
        """

        session = self.sm()
        try:
            task_count = session.query(Task).count()
        except:
            raise
        finally:
            session.close()

        return task_count

    def deleteAllTasks(self):
        """ Deletes all tasks

            :return: True if successful, False otherwise
            :rtype: boolean
        """

        session = self.sm()
        session.query(Task).delete(synchronize_session=False)
        session.commit()

        return True

    def updateTask(self, task_uuid, fields_to_update):
        """ This function inserts a new Task into the database.

            Usage:
                tasks.updateTask("12345-12345-1234-1234", {
                        "scheduled_time": datetime.strptime("2020-01-06 00:00:00", "%Y-%m-%d %H:%M:%S")
                    }


            :param task_uuid: The uuid of the task being changed
            :type task_uuid: str -- A UUID string

            :param fields_to_update: A key-value pair list of fields to update
            :type fields_to_update: dict() -- where key is the field name and the value is the new value

            :return: True if successful, False otherwise
            :rtype: boolean
        """

        session = self.sm()

        try:
            results = session.query(Task).\
                filter_by(uuid=task_uuid).\
                update(fields_to_update)

            print results
            session.commit()
        except:
            raise
        finally:
            session.close()

        return True

    def getActiveTasks(self, limit=None, current_time=datetime.utcnow()):
        """ Retrieve overdue tasks.

            :param limit: A limit to the number of tasks to return. None means no limit
            :type limit: int.

            :param current_time: An override for the current_time variable. This is used to
                retrieve overdue tasks
            :type current_time: datetime

            :return: A list of active tasks
            :rtype: A list() of Task objects
        """

        try:
            session = self.sm()

            session.commit()
            active_tasks = session.query(Task).\
                filter(Task.scheduled_time < current_time).\
                filter(Task.is_sent == 0).\
                filter(Task.is_failed == 0).\
                limit(limit).all()

        except:
            raise
        finally:
            pass

        """ TODO: Filter tasks by:
            (1) Last retry attempt is beyond set timeout value in config
        """

        return active_tasks

    def callTaskHTTPEndpoint(self, task):
        """ Call the task's HTTP Endpoint, flag last retry date and increment retry count

            Note: HTTP Endpoint MUST reply with a 200 OK response for the scheduler
                  to consider attempt a success

            If an error occurs, a SchedulerHTTPException with e.value and e.desc
            as summary and description for error, respectively.

            :param task: The task to trigger
            :type task: An instance of the Task object

            :return: True if HTTP Endpoint returned a 200 OK response, False otherwise
            :rtype: boolean.
        """

        self.logger.debug("Task: %s" % task.uuid)
        self.logger.debug("URL: %s" % task.endpoint_url)
        self.logger.debug("Method: %s" % task.endpoint_method)

        try:
            results = self.sendHTTPRequest(
                url=task.endpoint_url,
                method=task.endpoint_method,
                headers=task.endpoint_headers,
                body=task.endpoint_body)

            if results is True:
                # If sending was successful, flag task as sent, save sent_date
                self.setTaskAsSent(task_uuid=task.uuid)
                return True
            else:
                self.logger.debug("Attempt is Fail 0: %s" % task.uuid)
                raise SchedulerHTTPException("Endpoint did not reply with a HTTP 200 Response")

        except SchedulerHTTPException:
            """ If HTTP Exception, increment task's retry count, update last_retry_date,
                then re-raise exception
            """
            self.logger.info("Try")
            self.setTaskSendAttemptAsFail(task_uuid=task.uuid)
            raise

        except:
            self.logger.exception("Attempt is Fail 2: %s" % task.uuid)
            self.setTaskSendAttemptAsFail(task_uuid=task.uuid)
            raise

    def setTaskSendAttemptAsFail(self, task_uuid):
        session = self.sm()

        try:
            task = session.query(Task).filter_by(uuid=task_uuid).limit(1).first()
            task.is_sent = False
            task.retry_count = task.retry_count + 1
            task.last_retry_date = datetime.utcnow()

            if task.retry_count == task.max_retry_count:
                task.is_failed = True

            session.commit()
            return True
        except:
            raise
        finally:
            session.close()

    def setTaskAsSent(self, task_uuid):
        session = self.sm()

        try:
            session.query(Task).\
                filter(Task.uuid == task_uuid).\
                update({"is_sent": True,
                        "sent_date": datetime.utcnow()})
            session.commit()
            return True
        except:
            return False
        finally:
            session.close()

    def sendHTTPRequest(self, url, method, headers=None, body=None):
        # Build HTTP Request
        req = Request2(url, method=method)

        # Add Headers
        if isinstance(headers, dict):
            for h_name, h_val in headers.iteritems():
                req.add_header(h_name, h_val)
        else:
            self.logger.info("No headers")

        try:
            response = urllib2.urlopen(req, data=body)
            code = response.getcode()

            if code == 200:
                print response.read()
                return True
            else:
                raise SchedulerHTTPException("Endpoint did not reply with an HTTP 200 Response")

        except urllib2.HTTPError, e:
            raise SchedulerHTTPException("HTTP Error: %s" % str(e.code), desc=e.read())
        except urllib2.URLError, e:
            raise SchedulerHTTPException("URL Error: %s" % str(e.reason))
        except httplib.HTTPException, e:
            raise SchedulerHTTPException("HTTP Exception")
        except Exception:
            raise

if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///db/test.db', echo=True)
    tasks = TaskLogic(db_engine=engine)

    data_past = {
        "scheduled_time": datetime.utcnow() - timedelta(hours=1),
        "endpoint_url": "http://headers.jsontest.com/",
        "endpoint_headers": {
            "Content-Length": 0
        },
        "endpoint_body": "Test Body",
        "endpoint_method": "POST",
        "max_retry_count": 5
    }

    task_uuid = tasks.createTask(
        scheduled_time=data_past["scheduled_time"],
        endpoint_url=data_past["endpoint_url"],
        endpoint_headers=data_past["endpoint_headers"],
        endpoint_body=data_past["endpoint_body"],
        endpoint_method=data_past["endpoint_method"],
        max_retry_count=data_past["max_retry_count"])