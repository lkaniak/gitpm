# this file holds the custom Excpetions for the server. Add here and import in the viewset/model for usage.

import sys, traceback

class CommitsNotFound(Exception):
    def __init__(self):
        self.message = 'Could not find commits to work on. '
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.errors = traceback.format_exception(
          exc_type,
          exc_value,
          exc_traceback)
    def __str__(self):
        return self.message

class GenericException(Exception):
    def __init__(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.message = 'pmController error'
        self.errors = traceback.format_exception(
          exc_type,
          exc_value,
          exc_traceback)
    def __str__(self):
        return self.message


