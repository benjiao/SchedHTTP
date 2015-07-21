import json
from flask import Blueprint
from flask import current_app
from flask import make_response
from flask import request
from datetime import datetime


mod_tasks = Blueprint('mod_tasks', __name__)


@mod_tasks.route("/", methods=["POST"])
def createTask():
    """
    Creates a new task

    Sample Request:

    Headers:
        Accept: application/vnd.api+json
        Content-Type: application/vnd.api+json

    Body:
        {
            "data": {
                "attributes": {
                    "scheduled_time": "2015-07-12 00:00:00",
                    "endpoint_body": "{\"name\": \"Benjie\"}",
                    "endpoint_headers": {
                        "Content-Type": "application/json"
                    },
                    "endpoint_method": "POST",
                    "endpoint_url": "http://example.com/endpoint/",
                    "max_retry_count": 2
                },
                "type": "task"
            }
        }
    """

    try:
        data = json.loads(request.data)
        attributes = data["data"]["attributes"]
    except:
        return make_response("Invalid Data Format!", 400)

    current_app.logger.info("Data: %s", json.dumps(data, indent=4))

    # Check required fields before moving on
    try:
        scheduled_time = attributes["scheduled_time"]
        endpoint_url = attributes["endpoint_url"]
        endpoint_method = attributes["endpoint_method"]
    except:
        response = make_response("Required parameters might be missing", 403)
        return response

    endpoint_headers = attributes.get("endpoint_headers")
    endpoint_body = attributes.get("endpoint_body")
    max_retry_count = attributes.get("max_retry_count", 5)

    # Check if timestamp is in correct format
    try:
        scheduled_time_dt = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
    except:
        response = make_response("Timestamps should be in YYYY-MM-DD HH:MM:SS format", 403)
        return response

    # Proceed with creating a task
    task_uuid = current_app.tasks.createTask(
        scheduled_time=scheduled_time_dt,
        endpoint_url=endpoint_url,
        endpoint_headers=endpoint_headers,
        endpoint_body=endpoint_body,
        endpoint_method=endpoint_method,
        max_retry_count=max_retry_count)

    current_app.logger.info("Task Created: %s", task_uuid)

    response_body = {
        "data": {
            "type": "tasks",
            "attributes": {
                "id": task_uuid,
                "scheduled_time": scheduled_time,
                "endpoint_url": endpoint_url,
                "endpoint_headers": endpoint_headers,
                "endpoint_body": endpoint_body,
                "endpoint_method": endpoint_method,
                "max_retry_count": max_retry_count
            },
            "links": [
                'http://localhost/tasks/%s' % task_uuid
            ]
        }
    }

    response = make_response(json.dumps(response_body), 201)
    response.headers['Location'] = 'http://localhost/tasks/'
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
                'http://localhost/tasks/'
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
                'http://localhost/tasks/'
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
