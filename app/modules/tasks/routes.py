import json
from flask import Blueprint
from flask import make_response

mod_tasks = Blueprint('mod_tasks', __name__)


@mod_tasks.route("/", methods=["GET"])
def getTasks():
    """
    Returns a list of all tasks
    """

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


@mod_tasks.route("/", methods=["POST"])
def createTask():
    """
    Creates a new task
    """
    return json.dumps({"data": ""})


@mod_tasks.route("/<task_id>", methods=["GET"])
def getTask(task_id):
    """
    Returns details about a specific task
    """

    return json.dumps({"data": ""})


@mod_tasks.route("/<task_id>", methods=["DELETE"])
def deleteTask(task_id):
    return json.dumps({"data": ""})


@mod_tasks.route("/<task_id>", methods=["PATCH"])
def updateTask(task_id):
    return json.dumps({"data": ""})
