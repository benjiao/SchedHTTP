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

    task_uuid = "5e9003e1-2981-43d3-b8bb-6d5571dc53a3"
    url = "http://localhost:5000/tasks/%s" % task_uuid
    req = Request2(url, method="GET")
    req.add_header('Accept', 'application/vnd.api+json')

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        if code == 200:
            response_json = json.loads(response.read())
            print json.dumps(response_json, indent=4)

    except Exception, e:
        logging.exception("Error!")
