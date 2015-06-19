import json
from flask import Blueprint
from flask import make_response

mod_tasks = Blueprint('mod_tasks', __name__)


@mod_tasks.route("/", methods=["POST"])
def createTask():
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
