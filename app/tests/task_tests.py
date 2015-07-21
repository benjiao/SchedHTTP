"""
Scripts for testing the tasks.TaskLogic module
"""

import unittest
from datetime import datetime
from sqlalchemy import create_engine
from ..models import Task
from ..tasks import TaskLogic


class TestTasksCrud(unittest.TestCase):

    def test_create_and_delete(self):
        print "\n[TestTasksCrud] - Create and Delete"

        data = {
            "scheduled_time": datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            "endpoint_url": "http://test.com/test",
            "endpoint_headers": {
                "Authentication": "Test:Testing"
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
            "endpoint_url": "http://test.com/test",
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
            "endpoint_url": "http://test.com/test",
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
