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
    request_body = {
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

    url = "http://localhost:5000/tasks/"
    method = "POST"
    req = Request2(url, method, data=json.dumps(request_body))
    req.add_header('Content-type', 'application/vnd.api+json')
    req.add_header('Accept', 'application/vnd.api+json')

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        if code == 201:
            response = urllib2.urlopen(req)

            response_json = json.loads(response.read())
            print json.dumps(response_json, indent=4)

    except:
        pass
