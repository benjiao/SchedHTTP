import json
import urllib2


class Request2(urllib2.Request):
    def __init__(self, url, method, data=None, headers={}):
        self._method = method
        urllib2.Request.__init__(self, url=url, headers=headers, data=data)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)

if __name__ == '__main__':
    import logging

    request_body = {
        "data": {
            "attributes": {
                "scheduled_time": "2015-07-12 00:00:00",
                "endpoint_method": "POST",
                "endpoint_url": "http://localhost/asdfasdfqwerqwerasdfasdf",
                "max_retry_count": 2
            },
            "type": "task"
        }
    }

    url = "http://localhost:5000/tasks/"
    req = Request2(url, method="POST", data=json.dumps(request_body))
    req.add_header('Content-type', 'application/vnd.api+json')
    req.add_header('Accept', 'application/vnd.api+json')

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        if code == 201:
            response_json = json.loads(response.read())
            print json.dumps(response_json, indent=4)

    except:
        logging.exception("Error!")
