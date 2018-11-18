# this script is a controller for Process Mining features.

import sys
from halo import Halo
from pymongo import MongoClient

from githubAPI import main as githubAPI
from logBuilder import mainApp as Builder
from logBuilder.tools.csv_json2xes import generate_xes

from utils.ext_miner import callProcessMiner, readJSON, readDOT

from os import environ
from dotenv import load_dotenv
load_dotenv()


def requestRepoFromDatabase(onwer, repoName):
    '''django fetch commits caller'''
    return db['repositories'].find_one({'onwer': onwer, 'name': repoName})

def requestRepoFromGithub(**kwargs):
    '''github API fetch commits caller'''
    return githubAPI.main(repo=kwargs['repo'],
      onwer=kwargs['onwer'])

#E1: get the commits
def getCommits(url):
    '''commits controller caller (local version)'''
    mirrorUrl = list(reversed(url.split('/')))
    repo = mirrorUrl.pop(0)
    repoOnwer = mirrorUrl.pop(0)
    print('requesting commits from database. . .')
    commits = requestRepoFromDatabase(repoOnwer, repo)
    if not commits:
        with Halo(text='Requesting commits from Github. . .', spinner='dots'):
            commits = requestRepoFromGithub(onwer=repoOnwer, repo=repo)
        db['repositories'].insert_one({
            'onwer': repoOnwer,
            'name': repo,
            'commits': commits
        })
    return commits

# E2: generate the Event Log
def generateEventLog(**kwargs):
    '''Event Log controller caller'''
    log = Builder.miner(commits=kwargs['commits'], minCommits=kwargs.get('minCommits', None))
    Builder.writeCSV(log, kwargs.get('logName', 'teste'))
    return log

# E3: discover the process
def generateProcess(**kwargs):
    '''Process Discover controller caller'''
    parsedTime = kwargs.get('parsedTime', False)
    generate_xes(log=kwargs['log'], outputFile='{}{}'.format(environ.get('TEMPDIR_PATH'), kwargs['logName']), parsedTime=parsedTime)
    callProcessMiner(
        pathToMiner='{}minerful'.format(environ.get('PROMAPI_PATH')),
        logName=kwargs['logName'],
        tempDir=environ.get('TEMPDIR_PATH'),
        params=kwargs.get('params', []))
    process = readJSON('{}{}.json'.format(environ.get('TEMPDIR_PATH'), (kwargs['logName'])))
    if 'automaton' in kwargs.get('params', []):
        process['automaton'] = readDOT('{}{}.dot'.format(environ.get('TEMPDIR_PATH'), kwargs['logName']))
    return process


def main(url):
    '''local run only'''
    commits = getCommits(url)
    with Halo(text='Generating event log. . .', spinner='dots'):
        log = generateEventLog(commits=commits)

if __name__ == "__main__":
    main(sys.argv[1])
