from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from gitpm.models import (EventLog, EventLogFields, Repository)
from bson.objectid import ObjectId

def get_eventLog_name(log_name):
  try:
    logName = EventLog.objects.filter(
      name=log_name).only('name')
    return list(logName)
  except ObjectDoesNotExist:
    return None

def validate_name(log_name):
    message = ''
    modified = False
    logName = log_name
    while get_eventLog_name(logName):
      modified = True
      if '_copy' in logName:
        op = logName.split('_copy')
        logName = op[0] + '_copy' + str(int(op[1]) + 1)
      else:
        logName += '_copy1'

    if modified:
      message = 'A log with the name provided already exists, changed name to {}'.format(logName)
    return {
      'logName': logName,
      'message': message,
      'modified': modified
    }

def get_repositoryInEventLog(log_name):
  log = list(EventLog.objects.filter(
    name=log_name))
  if len(log) > 1:
    raise IntegrityError
  log = log[0]
  repo = list(Repository.objects.filter(
    _id=ObjectId(log.repository_id)
  ))
  return repo[0]

def get_eventLog(log_name):
  log = list(EventLog.objects.filter(
      name=log_name))
  if len(log) > 1:
    raise IntegrityError
  logEntries = list(EventLogFields.objects.filter(
    log=log[0]._id
  ))
  return {'log': log, 'entries': logEntries}

