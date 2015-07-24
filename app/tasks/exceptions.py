class SchedulerTasksException(Exception):
    pass


class SchedulerHTTPException(SchedulerTasksException):
    def __init__(self, value, desc=None):
        self.value = value
        self.desc = desc

    def __str__(self):
        return repr(self.value)
