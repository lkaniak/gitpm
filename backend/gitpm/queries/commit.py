from django.core.exceptions import ObjectDoesNotExist
from githubAPI import main as githubAPI
from gitpm.models import (Repository, Commit)
from bson.objectid import ObjectId

def get_commits_from_db(repo, repoOnwer):
  try:
    Repository.objects.get(
      name=repo,
      onwer=repoOnwer)
    commits = Commit.objects.filter(
      repository__name=repo,
      repository__onwer=repoOnwer)
    return list(commits)
  except ObjectDoesNotExist:
    return None

def get_repositoryFromCommit(repo_id):
  repo = Repository.objects.get(
    _id=ObjectId(repo_id))
  return repo

def get_commits_from_api(repo, repoOnwer):
  try:
    commits = githubAPI.main(
      repo=repo,
      owner=repoOnwer)
    return commits
  except Exception as e:
    raise e