"""
Scripts for testing the tasks.TaskLogic module
"""

import unittest
from datetime import datetime
from datetime import timedelta
from sqlalchemy import create_engine
from ..models import Task
from ..tasks import TaskLogic
from ..tasks import SchedulerHTTPException


class TestTasksCrud(unittest.TestCase):

    def test_create_and_delete(self):
        print "\n[TestTasksCrud] - Create and Delete"

        data = {
            "scheduled_time": datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": {
                "Content-Length": 0
            },
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        # Create test task
        task_uuid = tasks.createTask(
            scheduled_time=data["scheduled_time"],
            endpoint_url=data["endpoint_url"],
            endpoint_headers=data["endpoint_headers"],
            endpoint_body=data["endpoint_body"],
            endpoint_method=data["endpoint_method"],
            max_retry_count=data["max_retry_count"])

        self.assertIsInstance(task_uuid, str)

        # Check if the task created can be retrieved from the DB
        task_retrieved = tasks.getTaskByUUID(task_uuid)
        self.assertIsInstance(task_retrieved, Task)

        # Compare values
        self.assertEqual(task_retrieved.scheduled_time, data["scheduled_time"])
        self.assertEqual(task_retrieved.endpoint_url, data["endpoint_url"])
        self.assertEqual(task_retrieved.endpoint_headers, data["endpoint_headers"])
        self.assertEqual(task_retrieved.endpoint_body, data["endpoint_body"])
        self.assertEqual(task_retrieved.endpoint_method, data["endpoint_method"])
        self.assertEqual(task_retrieved.max_retry_count, data["max_retry_count"])

        # Check Default Values
        self.assertFalse(task_retrieved.is_sent)
        self.assertFalse(task_retrieved.is_failed)
        self.assertIsNone(task_retrieved.sent_date)
        self.assertEqual(task_retrieved.retry_count, 0)
        self.assertIsInstance(task_retrieved.created_date, datetime)
        self.assertIsNone(task_retrieved.last_retry_date)

        # Delete Task
        delete_return = tasks.deleteTaskByUUID(task_uuid)
        self.assertTrue(delete_return)

        # Confirm that deleted task is gone
        task_retrieved = tasks.getTaskByUUID(task_uuid)
        self.assertIsNone(task_retrieved)

        # Delete all tasks
        tasks.deleteAllTasks()

    def test_count_and_delete_all(self):
        print "\n[TestTasksCrud] - Count and Delete All"
        data = {
            "scheduled_time": datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        # Delete current tasks in the test database
        delete_results = tasks.deleteAllTasks()

        # Get current task count
        task_count = tasks.getTaskCount()
        self.assertIsInstance(task_count, int)
        self.assertEqual(task_count, 0)

        # Insert dummy data
        for x in xrange(5):
            tasks.createTask(
                scheduled_time=data["scheduled_time"],
                endpoint_url=data["endpoint_url"],
                endpoint_headers=data["endpoint_headers"],
                endpoint_body=data["endpoint_body"],
                endpoint_method=data["endpoint_method"],
                max_retry_count=data["max_retry_count"])

        # Get new task count
        task_count2 = tasks.getTaskCount()
        self.assertEqual(task_count2, (task_count + 5))

        # Delete all tasks
        delete_results = tasks.deleteAllTasks()
        self.assertTrue(delete_results)
        task_count3 = tasks.getTaskCount()
        self.assertEqual(task_count3, 0)

    def test_update(self):
        print "\n[TestTasksCrud] - Update"

        data = {
            "scheduled_time": datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        # Create original task
        original_uuid = tasks.createTask(
            scheduled_time=data["scheduled_time"],
            endpoint_url=data["endpoint_url"],
            endpoint_headers=data["endpoint_headers"],
            endpoint_body=data["endpoint_body"],
            endpoint_method=data["endpoint_method"],
            max_retry_count=data["max_retry_count"])

        # Compare original task values
        original_task = tasks.getTaskByUUID(task_uuid=original_uuid)
        self.assertEqual(original_task.scheduled_time, data["scheduled_time"])
        self.assertEqual(original_task.endpoint_url, data["endpoint_url"])
        self.assertEqual(original_task.endpoint_headers, data["endpoint_headers"])
        self.assertEqual(original_task.endpoint_body, data["endpoint_body"])
        self.assertEqual(original_task.endpoint_method, data["endpoint_method"])
        self.assertEqual(original_task.max_retry_count, data["max_retry_count"])

        # Update task scheduled_time
        new_scheduled_time = datetime.strptime("2020-01-03 00:00:00", "%Y-%m-%d %H:%M:%S")
        tasks.updateTask(original_uuid, {
            "scheduled_time": new_scheduled_time,
            })

        updated_task = tasks.getTaskByUUID(task_uuid=original_uuid)
        self.assertEqual(updated_task.scheduled_time, new_scheduled_time)

        # Delete all tasks
        tasks.deleteAllTasks()


class TestTaskDaemonFunctions(unittest.TestCase):
    def test_get_active_tasks(self):
        """ getActiveTasks must return all active tasks if limit is not set/None
        """

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        data_past = {
            "scheduled_time": datetime.utcnow() - timedelta(days=1),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        data_future = {
            "scheduled_time": datetime.utcnow() + timedelta(days=1),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        # Clear DB for good measure
        tasks.deleteAllTasks()

        # Insert 8 tasks set in the past
        for x in xrange(8):
            tasks.createTask(
                scheduled_time=data_past["scheduled_time"],
                endpoint_url=data_past["endpoint_url"],
                endpoint_headers=data_past["endpoint_headers"],
                endpoint_body=data_past["endpoint_body"],
                endpoint_method=data_past["endpoint_method"],
                max_retry_count=data_past["max_retry_count"])

        # Insert 4 tasks set in the future
        for x in xrange(4):
            tasks.createTask(
                scheduled_time=data_future["scheduled_time"],
                endpoint_url=data_future["endpoint_url"],
                endpoint_headers=data_future["endpoint_headers"],
                endpoint_body=data_future["endpoint_body"],
                endpoint_method=data_future["endpoint_method"],
                max_retry_count=data_future["max_retry_count"])

        active_tasks_all = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks_all), 8)

        tasks.deleteAllTasks()

    def test_get_active_tasks_with_limit(self):
        """ getActiveTasks must follow limit if it is set
        """

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        data_past = {
            "scheduled_time": datetime.utcnow() - timedelta(days=1),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        data_future = {
            "scheduled_time": datetime.utcnow() + timedelta(days=1),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        # Clear DB for good measure
        tasks.deleteAllTasks()

        # Insert 8 tasks set in the past
        for x in xrange(8):
            tasks.createTask(
                scheduled_time=data_past["scheduled_time"],
                endpoint_url=data_past["endpoint_url"],
                endpoint_headers=data_past["endpoint_headers"],
                endpoint_body=data_past["endpoint_body"],
                endpoint_method=data_past["endpoint_method"],
                max_retry_count=data_past["max_retry_count"])

        # Insert 4 tasks set in the future
        for x in xrange(4):
            tasks.createTask(
                scheduled_time=data_future["scheduled_time"],
                endpoint_url=data_future["endpoint_url"],
                endpoint_headers=data_future["endpoint_headers"],
                endpoint_body=data_future["endpoint_body"],
                endpoint_method=data_future["endpoint_method"],
                max_retry_count=data_future["max_retry_count"])

        active_tasks = tasks.getActiveTasks(limit=5)
        self.assertEqual(len(active_tasks), 5)

        tasks.deleteAllTasks()

    def test_get_active_tasks_empty(self):
        """ getActiveTasks must return an empty list if no task is currently
            active
        """

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        tasks.deleteAllTasks()

        active_tasks = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks), 0)
        self.assertIsInstance(active_tasks, list)

    def test_call_task_http_endpoint(self):
        engine = create_engine('sqlite:///db/test.db', echo=False)
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

        task = tasks.getTaskByUUID(task_uuid)
        self.assertFalse(task.is_sent)
        self.assertFalse(task.is_failed)
        self.assertIsNone(task.sent_date)
        self.assertEqual(task.retry_count, 0)

        results = tasks.callTaskHTTPEndpoint(task)
        self.assertTrue(results)

        task_after_call = tasks.getTaskByUUID(task_uuid)
        self.assertTrue(task_after_call.is_sent)
        self.assertIsInstance(task_after_call.sent_date, datetime)

        tasks.deleteAllTasks()

    def test_call_task_http_endpoint_fail(self):
        """ On failed call to HTTP Endpoint,
            the service must increment retry_count on db
            the last_retry_date field should also be updated

            This test tests the setTaskSendAttemptAsFail function via
            actual HTTP call fails
        """

        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        data_past = {
            "scheduled_time": datetime.utcnow() - timedelta(hours=1),
            "endpoint_url": "http://localhost/qwerpoiuasddfjasld",
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        task_uuid = tasks.createTask(
            scheduled_time=data_past["scheduled_time"],
            endpoint_url=data_past["endpoint_url"],
            endpoint_headers=None,
            endpoint_body=data_past["endpoint_body"],
            endpoint_method=data_past["endpoint_method"],
            max_retry_count=data_past["max_retry_count"])

        task = tasks.getTaskByUUID(task_uuid)
        print task.uuid
        print task.endpoint_url
        print str(task.endpoint_headers)

        with self.assertRaises(SchedulerHTTPException):
            tasks.callTaskHTTPEndpoint(task)

        task_after_call = tasks.getTaskByUUID(task_uuid)
        self.assertFalse(task_after_call.is_sent)
        self.assertIsNone(task_after_call.sent_date)
        self.assertEqual(task_after_call.retry_count, 1)
        self.assertIsInstance(task_after_call.last_retry_date, datetime)

        tasks.deleteAllTasks()

    def test_increment_retry_count_on_fail(self):
        """ On failed call to HTTP Endpoint,
            the service must increment retry_count on db
            the last_retry_date field should also be updated

            This test tests the setTaskSendAttemptAsFail function manually
        """
        engine = create_engine('sqlite:///db/test.db', echo=False)
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

        tasks.setTaskSendAttemptAsFail(task_uuid)

        task_after = tasks.getTaskByUUID(task_uuid)
        self.assertEqual(task_after.retry_count, 1)
        self.assertIsInstance(task_after.last_retry_date, datetime)

        old_retry_date = task_after.last_retry_date

        tasks.setTaskSendAttemptAsFail(task_uuid)

        task_after2 = tasks.getTaskByUUID(task_uuid)
        self.assertEqual(task_after2.retry_count, 2)
        self.assertIsInstance(task_after2.last_retry_date, datetime)
        self.assertNotEqual(task_after2.last_retry_date, old_retry_date)

    def test_get_active_tasks_retry_limit(self):
        """ Only tasks that are below their retry limits should be
            returned by getActiveTasks
        """
        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        data_past = {
            "scheduled_time": datetime.utcnow() - timedelta(hours=1),
            "endpoint_url": "http://localhost/asdfasdfwqerqwerzcxvzxcv",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 3
        }

        task_uuid = tasks.createTask(
            scheduled_time=data_past["scheduled_time"],
            endpoint_url=data_past["endpoint_url"],
            endpoint_headers=data_past["endpoint_headers"],
            endpoint_body=data_past["endpoint_body"],
            endpoint_method=data_past["endpoint_method"],
            max_retry_count=data_past["max_retry_count"])

        tasks.createTask(
            scheduled_time=data_past["scheduled_time"],
            endpoint_url=data_past["endpoint_url"],
            endpoint_headers=data_past["endpoint_headers"],
            endpoint_body=data_past["endpoint_body"],
            endpoint_method=data_past["endpoint_method"],
            max_retry_count=data_past["max_retry_count"])

        # First attempt
        task1 = tasks.getTaskByUUID(task_uuid)
        with self.assertRaises(SchedulerHTTPException):
            tasks.callTaskHTTPEndpoint(task1)
        active_tasks1 = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks1), 2)

        # Second attempt
        task2 = tasks.getTaskByUUID(task_uuid)
        with self.assertRaises(SchedulerHTTPException):
            tasks.callTaskHTTPEndpoint(task2)
        active_tasks2 = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks2), 2)

        # Third attempt MUST NOT return the failing task anymore
        task3 = tasks.getTaskByUUID(task_uuid)
        with self.assertRaises(SchedulerHTTPException):
            tasks.callTaskHTTPEndpoint(task3)
        active_tasks3 = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks3), 1)

        # Verify that task's is_failed flag is True after max attempt
        failed_task = tasks.getTaskByUUID(task_uuid)
        self.assertTrue(failed_task.is_failed)

    def test_get_active_tasks_no_is_sent(self):
        """ Tasks with the is_sent flag should not be included in getActiveTasks
            results
        """
        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        data_past = {
            "scheduled_time": datetime.utcnow() - timedelta(hours=1),
            "endpoint_url": "http://headers.jsontest.com/",
            "endpoint_headers": None,
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

        task_uuid2 = tasks.createTask(
            scheduled_time=data_past["scheduled_time"],
            endpoint_url=data_past["endpoint_url"],
            endpoint_headers=data_past["endpoint_headers"],
            endpoint_body=data_past["endpoint_body"],
            endpoint_method=data_past["endpoint_method"],
            max_retry_count=data_past["max_retry_count"])

        active_tasks = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks), 2)

        # Send first task
        task1 = tasks.getTaskByUUID(task_uuid)
        tasks.callTaskHTTPEndpoint(task1)

        active_tasks_after_call = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks_after_call), 1)
        self.assertEqual(active_tasks_after_call[0].uuid, task_uuid2)

        # Send second task
        task2 = tasks.getTaskByUUID(task_uuid2)
        tasks.callTaskHTTPEndpoint(task2)

        active_tasks_after_call2 = tasks.getActiveTasks()
        self.assertEqual(len(active_tasks_after_call2), 0)

        tasks.deleteAllTasks()


class TestTaskHTTPFunctions(unittest.TestCase):
    def test_request_post(self):
        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        url = "http://headers.jsontest.com/"
        method = "POST"
        headers = {
            "Content-Length": 0
        }

        results = tasks.sendHTTPRequest(url=url,
                                        method=method,
                                        headers=headers)

        self.assertTrue(results)

    def test_request_post_fail(self):
        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        url = "http://localhost/asdfasdfwqerqwerzcxvzxcv"
        method = "POST"

        with self.assertRaises(SchedulerHTTPException):
            tasks.sendHTTPRequest(url=url, method=method)

    def test_request_post_fail_flags(self):
        engine = create_engine('sqlite:///db/test.db', echo=False)
        tasks = TaskLogic(db_engine=engine)

        # Note: Calling this endpoint without the Content-Length error
        #       returns an error
        url = "http://headers.jsontest.com/"
        method = "POST"

        with self.assertRaises(SchedulerHTTPException):
            tasks.sendHTTPRequest(url=url, method=method)
