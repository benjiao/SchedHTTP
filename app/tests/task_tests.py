import unittest
from sqlalchemy import create_engine
from models import Task
from tasks import TaskLogic


class TestTasksCrud(unittest.TestCase):
    def test_create_and_delete(self):
        data = {
            "scheduled_time": "2020-01-01 00:00:00",
            "endpoint_url": "http://test.com/test",
            "endpoint_headers": None,
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5
        }

        engine = create_engine('sqlite:///app.db', echo=True)
        tasks = TaskLogic(db_engine=engine)

        # Create test task
        print "Create Task"
        task_uuid = tasks.createTask(
            scheduled_time=data["scheduled_time"],
            endpoint_url=data["endpoint_url"],
            endpoint_headers=data["endpoint_headers"],
            endpoint_body=data["endpoint_body"],
            endpoint_method=data["endpoint_method"],
            max_retry_count=data["max_retry_count"])

        self.assertIsInstance(task_uuid, str)

        # Check if the task created can be retrieved from the DB
        print "Retrieve created task. UUID: %s" % task_uuid
        task_retrieved = tasks.getTaskByUUID(task_uuid)
        self.assertIsInstance(task_retrieved, Task)

        # Compare values
        print "Check values"
        self.assertEqual(task_retrieved.scheduled_time, data["scheduled_time"])
        self.assertEqual(task_retrieved.endpoint_url, data["endpoint_url"])
        self.assertEqual(task_retrieved.endpoint_headers, data["endpoint_headers"])
        self.assertEqual(task_retrieved.endpoint_body, data["endpoint_body"])
        self.assertEqual(task_retrieved.endpoint_method, data["endpoint_method"])
        self.assertEqual(task_retrieved.max_retry_count, data["max_retry_count"])

        # Delete Task
        print "Delete task"
        delete_return = tasks.deleteTaskByUUID(task_uuid)
        self.assertTrue(delete_return)

        # Confirm that deleted task is gone
        print "Confrim deletion"
        task_retrieved = tasks.getTaskByUUID(task_uuid)
        self.assertIsNone(task_retrieved)
