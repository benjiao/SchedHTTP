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

    task_uuid = "d98ea285-902c-44f5-b264-de9bd2c11473"

    url = "http://localhost:6500/tasks/%s" % task_uuid
    req = Request2(url, method="DELETE")
    req.add_header('Accept', 'application/vnd.api+json')

    try:
        response = urllib2.urlopen(req)
        code = response.getcode()

        if code == 200:
            print response.read()

    except:
        logging.exception("Error!")
