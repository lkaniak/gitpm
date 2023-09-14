# this file is a controller for the github API interaction.

from __future__ import print_function
import sys
from .helpers.external import requestCommits

from os import environ
from dotenv import load_dotenv
load_dotenv()

def main(**kwargs):
  try:
    pageSize = 20
    apikey = environ.get('GITAUTH')

    if apikey is None:
      raise ValueError("API key required to make requests was not found.")

    apiurl = environ.get('GITHUB_APIURL')
    if apiurl is None:
      raise ValueError("API url not found.")
    #H1
    commits = requestCommits(
        repository=kwargs['repo'],
        repoOnwer=kwargs['owner'],
        pageSize=pageSize,
        hasNextPage='First Page',
        apiurl=apiurl,
        apikey=apikey)

    return commits
  except Exception as e:
    raise e

if __name__ == "__main__":
  main(sys.argv[1])
