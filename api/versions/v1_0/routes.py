import json
from flask import Blueprint
from flask import make_response

api = Blueprint('api', __name__)


@api.route("/task", methods=["POST"])
def createTask():
    """
    Request:

    ```
    {
        "data": {
            "time": "2015-03-10 00:00:00",
            "callbackType": "http",
            "callback": {
                "url": "http://127.0.0.1/sendEmail",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer rmJxSsIlzoK05BWkQSWf1NiWMaMN"
                },
                "body": "client_id=NXuLLPp30VgTtA4XL02P87lMvLKbrk2U&client_secret=uG2vGZ3M1rpXOtBZ&grant_type=client_credentials"
            }
        }
    }
    ```
    """
    
    
    response_body = {
        "data": {
            "type": "task",
            "attributes": {
                "time": 
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

