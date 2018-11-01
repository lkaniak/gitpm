import json
from datetime import datetime

import pmController, os

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *

from djongo import models
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db import InternalError

from .models import (User, Repository, Commit, ModifiedFiles, EventLogFields)
from githubAPI import main as githubAPI

from bson import Binary, Code
from bson.json_util import dumps

from .queries.commit import *
from .queries.logs import *

from os import environ
from dotenv import load_dotenv
load_dotenv()

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def list(self, request):
      pass

  def create(self, request):
    try:
      u = User(
        username=request.data['username'],
        password=request.data['pass'],
        name=request.data['name'],
        email=request.data['email'],
      )
      u.save()
      return Response({'status': 'user set'})
    except Exception as e:
      return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def retrieve(self, request, pk=None):
      pass

  def update(self, request, pk=None):
      pass

  def partial_update(self, request, pk=None):
      pass

  def destroy(self, request, pk=None):
      pass

class GitRepositoryViewSet(viewsets.ModelViewSet):
  queryset = Repository.objects.all()
  serializer_class = GitRepositorySerializer

  @action(detail=False, methods=['post'])
  def get_commits(self, request):
    mirrorUrl = list(reversed(request.data['url'].split('/')))
    repo = mirrorUrl.pop(0)
    repoOnwer = mirrorUrl.pop(0)
    commits = get_commits_from_db(repo, repoOnwer)
    if commits:
      serializer = CommitSerializer(commits, many=True)
      return HttpResponse(dumps(serializer.data))
    else:
      commits = get_commits_from_api(repo, repoOnwer)
      r = Repository(
        url=request.data['url'],
        name=repo,
        onwer=repoOnwer)
      try:
        r.save()
        for commit in commits:
          modifiedFiles = []
          for modifiedFile in commit['modifiedFiles']:
            modifiedFiles.append(ModifiedFiles(
              modifiedFile=modifiedFile['file'],
              additions=modifiedFile['additions'],
              changes=modifiedFile['changes'],
              deletions=modifiedFile['deletions'],
              status= modifiedFile['status']
            ))
          if 'Z' in commit['author']['date']:
            date = commit['author']['date']
          else:
            date = commit['author']['date'].rsplit(':', 1)
          c = Commit(
            repository=r,
            user=commit['author']['name'],
            hashID=commit['oid'],
            email=commit['author']['email'],
            date=''.join(date),
            message=commit['messageHeadline'],
            modifiedFiles=modifiedFiles
          )
          c.save()
        modeledCommits = get_commits_from_db(repo, repoOnwer)
        serializer = CommitSerializer(modeledCommits, many=True)
        return HttpResponse(dumps(serializer.data))
      except Exception as e:
        Repository.objects.filter(
          url=request.data['url'],
          name=repo,
          onwer=repoOnwer).delete()
        raise e

  @action(detail=False, methods=['post'])
  def download(self, request):
    mirrorUrl = list(reversed(request.data['url'].split('/')))
    repo = mirrorUrl.pop(0)
    repoOnwer = mirrorUrl.pop(0)
    commits = get_commits_from_db(repo, repoOnwer)
    if commits:
      serializer = CommitSerializer(commits, many=True)
      return HttpResponse(dumps(serializer.data))
    else:
      raise Http404

class EventLogViewSet(viewsets.ModelViewSet):
  queryset = EventLog.objects.all()
  serializer_class = EventLogSerializer

  @action(detail=False, methods=['post'])
  def generate_log(self, request):
    logName = None
    if 'logName' in request.data:
      logName = request.data['logName']
    warnings = []
    if not logName:
      warnings.append('log name not found. Defaulting to "test"')
      logName = 'test'
    nameValidation = validate_name(logName)
    if nameValidation['modified']:
      warnings.append(nameValidation['message'])
    mirrorUrl = list(reversed(request.data['url'].split('/')))
    repo = mirrorUrl.pop(0)
    repoOnwer = mirrorUrl.pop(0)
    commits = get_commits_from_db(repo, repoOnwer)
    if not commits:
      raise Exception('log generation: could not find commits for the specified repository.')
    log = pmController.generateEventLog(
      commits=commits,
      minCommits=request.data.get('minCommits', None),
      logName=nameValidation.get('logName', 'teste'))
    date = datetime.now()
    repo = get_repositoryFromCommit(commits[0].repository_id)
    l = EventLog(
      repository=repo,
      name=nameValidation['logName'],
      created_at=date
    )
    l.save()
    try:
      for rows in log.values():
        e = EventLogFields(
          log=l,
          caseID=rows['case'],
          activity=rows['activity'],
          timestamp=rows['timestamp'],
          commit=rows['commit']
        )
        e.save()
    except Exception as e:
        EventLog.objects.filter(
          name=logName,
          created_at=date).delete()
        raise e
    modeledLog = get_eventLog(nameValidation['logName'])
    serializerLog = EventLogSerializer(modeledLog['log'][0])
    serializerEntries = EventLogFieldsSerializer(modeledLog['entries'], many=True)
    response = {
      'message': 'Successfuly generated log.',
      'warnings': warnings,
      'log': {'log': serializerLog.data, 'entries': serializerEntries.data }
    }
    return JsonResponse(response)

  @action(detail=False, methods=['post'])
  def download(self, request):
    logName = None
    if 'logName' not in request.data:
      raise Http404
    logName = request.data['logName']
    repo = get_repositoryInEventLog(logName)
    file_path = '{}{}.csv'.format(environ.get('TEMPDIR_PATH'), logName)
    if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv")
        response['Content-Disposition'] = 'inline; filename={}-{}_{}'.format(repo.onwer, repo.name, os.path.basename(file_path))
        return response
    raise InternalError

class ProcessModelViewSet(viewsets.ModelViewSet):
  queryset = ProcessModel.objects.all()
  serializer_class = ProcessModelSerializer

  @action(detail=False, methods=['post'])
  def generate_process(self, request):
    logName = request.data['logName']
    if not logName or not get_eventLog_name(logName):
      raise Exception('process generation: could not find specified log.')
    modeledLog = get_eventLog(logName)
    serializerLog = EventLogSerializer(modeledLog['log'][0])
    serializerEntries = EventLogFieldsSerializer(modeledLog['entries'], many=True)
    logData = serializerLog.data
    logEntries = serializerEntries.data
    params = request.data.get('params', None)
    process = pmController.generateProcess(
      log=logEntries,
      logName=logData['name'],
      params=params)
    return JsonResponse(process)

  @action(detail=False, methods=['post'])
  def download(self, request):
    logName = None
    if 'logName' not in request.data:
      raise Http404
    logName = request.data['logName']
    modeledLog = get_eventLog(logName)
    repo = get_repositoryInEventLog(logName)
    file_path = '{}{}.xes'.format(environ.get('TEMPDIR_PATH'), logName)
    if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv")
        response['Content-Disposition'] = 'inline; filename={}-{}_{}'.format(repo.onwer, repo.name, os.path.basename(file_path))
        return response
    raise InternalError

