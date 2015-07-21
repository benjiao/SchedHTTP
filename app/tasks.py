import uuid
from datetime import datetime
from models import Task
from sqlalchemy.orm import sessionmaker


class TaskLogic:
    def __init__(self, db_engine):
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
        session.add(newtask)
        session.commit()

        return task_uuid

    def getTaskByUUID(self, task_uuid):
        """ Retrieves a specific Task using its UUID

        :param task_uuid: The task's UUID returned upon creation
        :type task_uuid: str -- A UUID string

        :retrun: The task
        :rtype: A Task object
        """

        session = self.sm()
        results = session.query(Task).filter_by(uuid=task_uuid).limit(1)

        return results.first()

    def deleteTaskByUUID(self, task_uuid):
        """ Deletes a task using its UUID

        :param task_uuid: The UUID of the task to be deleted
        :type task_uuid: str -- A UUID string

        :return: True if successful, False otherwise
        :rtype: boolean
        """

        session = self.sm()
        session.query(Task).filter_by(uuid=task_uuid).\
            delete(synchronize_session=False)
        session.commit()

        return True

    def getTaskCount(self, include_done=True):
        """ Retrieves the number of tasks currently in the DB

        :param include_done: Controls whether or not to include finished tasks in the count
        :type include_done: boolean

        :return: The number of tasks in the DB
        :rtype: int
        """

        session = self.sm()
        task_count = session.query(Task).count()
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

if __name__ == '__main__':
    from sqlalchemy import create_engine
    data = {
            "scheduled_time": "2020-01-01 00:00:00",
            "endpoint_url": "http://test.com/test",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

    engine = create_engine('sqlite:///db/test.db', echo=True)
    tasks = TaskLogic(db_engine=engine)

    tasks.createTask(
        scheduled_time=data["scheduled_time"],
        endpoint_url=data["endpoint_url"],
        endpoint_headers=data["endpoint_headers"],
        endpoint_body=data["endpoint_body"],
        endpoint_method=data["endpoint_method"],
        max_retry_count=data["max_retry_count"])
