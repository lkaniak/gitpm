#this file contains tools for the gitHub commit extraction

import json, requests
import concurrent.futures as cf

from .dict_json import recursive_get
from utils.timer import timing

from requests_futures.sessions import FuturesSession

from os import environ
from dotenv import load_dotenv
load_dotenv()

def requestsAsync(urls, header, pageSize):
  '''helper function to make async HTTP requests'''
  session = FuturesSession(executor=cf.ThreadPoolExecutor(max_workers=10))
  responses = {}
  for url in urls:
    request = session.get(url['url'], headers=header)
    responses[request] = { 'cHash': url['cHash'] }
  return responses

def getUrls(**kwargs):
  '''for each commit, generate a v3 call to get modifiedFiles'''
  urls = []
  for commit in kwargs['commits']:
    url = "https://api.github.com/repos/%s/%s/commits/%s" % (
      kwargs['onwer'],
      kwargs['repo'],
      commit['oid'])
    urls.append({ 'cHash': commit['oid'], 'url': url })
  return urls

def parseModifiedFiles(response, cHash):
  '''parse v3 response'''
  if response.status_code == 200:
    mFiles = []
    for file in response.json()['files']:
      modifiedFiles = [{
        'additions': file['additions'],
        'changes': file['changes'],
        'deletions': file['deletions'],
        'status': file['status'],
        'file': file['filename'],
      }]
      mFiles += modifiedFiles
    return { 'cHash': cHash, 'modifiedFiles': mFiles }
  else:
    response.raise_for_status()

# workaround to get modifiedFiles since v4 does not support as for the date of this file
def getModifiedFilesAsync(**kwargs):

  commits = kwargs['commits']

  HTTPheaders = {"Authorization": "Bearer {0}".format(kwargs['apikey'])}
  urls = getUrls(
    commits=commits,
    repo=kwargs['repo'],
    onwer=kwargs['onwer'])

  responses = requestsAsync(urls, HTTPheaders, kwargs['pageSize'])
  try:
    parsed = []
    for response in cf.as_completed(responses):
      parsed.append(parseModifiedFiles(response.result(), responses[response]['cHash']))

    for commit in commits:
      for modifiedFiles in parsed:
        if modifiedFiles['cHash'] == commit['oid']:
          commit['modifiedFiles'] = modifiedFiles['modifiedFiles']
  except Exception as e:
    raise e

  return commits

def getPagination(response):
  '''parse v4 pagination style'''
  parsedResponse = response.json()
  pageInfo = recursive_get(
      parsedResponse,
      'data',
      'repository',
      'ref',
      'target',
      'history',
      'pageInfo')
  return pageInfo

# workaround to get modifiedFiles since v4 does not support as for the date of this file
def getModifiedFiles(**kwargs):

  commits = kwargs['commits']

  HTTPheaders = {"Authorization": "Bearer {0}".format(kwargs['apikey'])}
  for commit in commits:
    url = "https://api.github.com/repos/%s/%s/commits/%s" % (
      kwargs['onwer'],
      kwargs['repo'],
      commit['oid'])
    response = requests.get(url, headers=HTTPheaders)
    if response.status_code == 200:
      commit['modifiedFiles'] = []
      for file in response.json()['files']:
        modifiedFiles = [{
          'additions': file['additions'],
          'changes': file['changes'],
          'deletions': file['deletions'],
          'status': file['status'],
          'file': file['filename'],
        }]
        commit['modifiedFiles'] += modifiedFiles
    else:
      response.raise_for_status()
  return commits

def extractCommits(response):
  '''parse v4 commit response'''
  parsedResponse = response.json()
  nodes = recursive_get(
      parsedResponse,
      'data',
      'repository',
      'ref',
      'target',
      'history',
      'edges')
  commits = list('')
  for node in nodes:
    commits.append(node['node'])
  return commits