# this file builds and executes the calls to the giitHub API

from __future__ import print_function
import json, requests, timeit
from requests import exceptions

from .queryHelpers import (getPagination, getModifiedFiles, extractCommits, getModifiedFilesAsync)

def requestCommits(**kwargs):
  '''
    recursive function to request commits from gitHub.
    function args:\n\n
    repository: Repository name\n
    repoOnwer: Repository onwer\n
    pageSize: Number of commits to get for each call, respecting V4's resource limitations\n
    hasNextPage: Object returned from the v4 API to indicate if there is more pages with commits.\n
    Its also used as stop condition and starts with a default value.
  '''
  if 'hasNextPage' not in kwargs:
    return list('')
  if kwargs['hasNextPage'] == 'First Page':
    pagination = ''
  else:
    pagination = ', after:"%s"' % (kwargs['hasNextPage']['endCursor'])

  query = '''
    query {
      repository(name: "%s", owner: "%s") {
        ref(qualifiedName: "master") {
          target {
            ... on Commit {
              id
              history(first: %s%s) {
                pageInfo {
                  startCursor
                  hasNextPage
                  endCursor
                }
                edges {
                  node {
                    messageHeadline
                    oid
                    message
                    changedFiles
                    author {
                      name
                      email
                      date
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ''' % (
      kwargs['repository'],
      kwargs['repoOnwer'],
      kwargs['pageSize'],
      pagination)

  response = runQuery(
    query=query,
    apikey=kwargs['apikey'],
    url=kwargs['apiurl'])
  if response.status_code is not 200:
    raise ValueError({
        "message": response.json(),
        "code": response.status_code
    })
  if 'errors' in response.json():
    raise ValueError({
        "message": response.json()['errors'],
        "code": 500
    })
  else:
    try:
      pageInfo = getPagination(response)
      commits = extractCommits(response)
      commits = getModifiedFilesAsync(
        commits=commits,
        repo=kwargs['repository'],
        onwer=kwargs['repoOnwer'],
        apikey=kwargs['apikey'],
        pageSize=kwargs['pageSize'])
      if pageInfo['hasNextPage'] is True:
        kwargs['hasNextPage'] = pageInfo
      else:
        kwargs.pop('hasNextPage')
      return requestCommits(**kwargs) + commits
    except Exception as e:
      raise e


def runQuery(**kwargs):
  try:

    HTTPheaders = {"Authorization": "Bearer {0}".format(kwargs['apikey'])}
    response = requests.post(kwargs['url'], json={'query': kwargs['query']}, headers=HTTPheaders)
    if response.status_code == 200:
      return response
    else:
      response.raise_for_status()

  except ValueError as e:
    print("Error({0}): Check if the variables were exported \
    correctly on environment." \
    .format(e))

  except requests.exceptions.RequestException as e:
    print("Error({0}): {1} Multiple errors in HTTP requests found." \
    .format(e.errno, e.strerror))

  except requests.exceptions.ConnectionError as e:
    print("Error({0}): {1} A Connection error occurred." \
    .format(e.errno, e.strerror))


  except requests.exceptions.HTTPError as e:
    print("Error({0}): {1} An HTTP error occurred." \
      .format(e.errno, e.strerror))
    return response

  except requests.exceptions.URLRequired as e:
    print("Error({0}): {1} A valid URL is required to make a request." \
      .format(e.errno, e.strerror))

  except requests.exceptions.TooManyRedirects as e:
    print("Error({0}): {1} Too many redirects.".format(e.errno, e.strerror))

  except requests.exceptions.ConnectTimeout as e:
    # TODO: RETRY METHOD
    print("Error({0}): {1} The request timed out while trying to \
    connect to the remote server.".format(e.errno, e.strerror))

  except requests.exceptions.ReadTimeout as e:
    print("Error({0}): {1} The server did not send any data \
    in the allotted amount of time.".format(e.errno, e.strerror))

  except requests.exceptions.Timeout as e:
    print("Error({0}): {1} The request timed out." \
      .format(e.errno, e.strerror))
