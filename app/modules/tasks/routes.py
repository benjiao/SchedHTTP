import json
from flask import Blueprint
from flask import current_app
from flask import make_response
from datetime import datetime


mod_tasks = Blueprint('mod_tasks', __name__)


@mod_tasks.route("/", methods=["POST"])
def createTask():
    """
    Creates a new task
    """

    current_app.logger.info("Create Task Called!")

    data = {"scheduled_time": datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"),
            "endpoint_url": "http://test.com/test",
            "endpoint_headers": {
                "Authentication": "Test:Testing"
            },
            "endpoint_body": "Test Body",
            "endpoint_method": "POST",
            "max_retry_count": 5}

    current_app.tasks.createTask(
        scheduled_time=data["scheduled_time"],
        endpoint_url=data["endpoint_url"],
        endpoint_headers=data["endpoint_headers"],
        endpoint_body=data["endpoint_body"],
        endpoint_method=data["endpoint_method"],
        max_retry_count=data["max_retry_count"])

    response_body = {
        "data": {
            "type": "task",
            "attributes": {
                "time": "2015-03-10 00:00:00"
            },
            "links": [
                'http://api.reach-social.com/v1.0/1'
            ]
        }
    }

    response = make_response(json.dumps(response_body), 201)
    response.headers['Location'] = 'http://api.reach-social.com/gnip/v1.0/1'
    response.headers['Content-Type'] = 'application/vnd.api+json'
    return response


@mod_tasks.route("/", methods=["GET"])
def getTasks():
    """
    Returns a list of all tasks
    """
    current_app.logger.info("Get Tasks Called!")

    response_body = {
        "data": {
            "type": "task",
            "attributes": {
                "time": "2015-03-10 00:00:00"
            },
            "links": [
                'http://api.reach-social.com/v1.0/1'
            ]
        }
    }

    response = make_response(json.dumps(response_body), 200)
    response.headers['Location'] = 'http://api.reach-social.com/gnip/v1.0/1'
    response.headers['Content-Type'] = 'application/vnd.api+json'
    return response


@mod_tasks.route("/<task_id>", methods=["GET"])
def getTask(task_id):
    """
    Returns details about a specific task
    """
    current_app.logger.info("Get Task Called!")

    response_body = {
        "data": {
            "type": "task",
            "attributes": {
                "time": "2015-03-10 00:00:00"
            },
            "links": [
                'http://api.reach-social.com/v1.0/1'
            ]
        }
    }
    response = make_response(json.dumps(response_body), 201)
    response.headers['Location'] = 'http://api.reach-social.com/gnip/v1.0/1'
    response.headers['Content-Type'] = 'application/vnd.api+json'
    return response


@mod_tasks.route("/<task_id>", methods=["DELETE"])
def deleteTask(task_id):
    current_app.logger.info("Delete Task Called!")
    return json.dumps({"data": ""})


@mod_tasks.route("/<task_id>", methods=["PATCH"])
def updateTask(task_id):
    current_app.logger.info("Update Task Called!")
    return json.dumps({"data": ""})
